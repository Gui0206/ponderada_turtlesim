#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
import numpy as np
import argparse
import time

from .image_processor import ImageProcessor


class TurtleDrawer(Node):
    """Nó ROS 2 que desenha contornos de imagem usando turtlesim com teleportação."""

    def __init__(self, image_path: str = None):
        super().__init__('turtle_drawer')

        self.image_path = image_path

        # Cria clientes de serviços
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')

        # Aguarda serviços
        while not self.teleport_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Aguardando serviço /turtle1/teleport_absolute...')

        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Aguardando serviço /turtle1/set_pen...')

        self.get_logger().info('Serviços prontos! Iniciando desenho...')

    def extract_points_from_binary_image(self, binary_image: np.ndarray) -> list:
        """Extrai todos os pixels brancos da imagem binária e mapeia para espaço turtle."""
        height, width = binary_image.shape

        # Encontra todos os pixels brancos
        y_indices, x_indices = np.where(binary_image == 255)

        if len(x_indices) == 0:
            self.get_logger().warn('Nenhum pixel branco encontrado na imagem')
            return []

        # Mapeia para espaço turtle com margens
        points = []
        margin = 0.5
        turtle_bounds = 11.0
        available_space = turtle_bounds - (2 * margin)

        min_x, max_x = np.min(x_indices), np.max(x_indices)
        min_y, max_y = np.min(y_indices), np.max(y_indices)

        # Calcula escala para caber no espaço turtle
        largest_dim = max(max_x - min_x, max_y - min_y)
        scale = available_space / (largest_dim + 1)

        for x, y in zip(x_indices, y_indices):
            # Mapeia para coordenadas turtle
            turtle_x = margin + (x - min_x) * scale
            turtle_y = margin + (max_y - y) * scale
            points.append((turtle_x, turtle_y))

        self.get_logger().info(f'Extraídos {len(points)} pontos da imagem')
        return points

    def teleport_turtle(self, x: float, y: float, theta: float = 0.0):
        """Teleporta a tartaruga para posição."""
        request = TeleportAbsolute.Request()
        request.x = x
        request.y = y
        request.theta = theta

        future = self.teleport_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def set_pen(self, r: int = 0, g: int = 0, b: int = 0, width: int = 1, off: int = 0):
        """Define propriedades da caneta (cor, largura, ativado/desativado)."""
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = self.pen_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def draw_image(self):
        """Função principal de desenho."""
        if self.image_path is None:
            self.get_logger().error('Caminho da imagem não definido')
            return False

        try:
            # Carrega imagem
            self.get_logger().info(f'Carregando imagem: {self.image_path}')
            image = ImageProcessor.load_image(self.image_path)
            self.get_logger().info(f'Dimensões da imagem: {image.shape}')

            # Pré-processamento
            self.get_logger().info('Pré-processando imagem...')
            binary = ImageProcessor.preprocess(image)

            # Extrai pontos
            self.get_logger().info('Extraindo pontos...')
            points = self.extract_points_from_binary_image(binary)

            if len(points) == 0:
                self.get_logger().warn('Nenhum ponto para desenhar')
                return False

            # Desenha
            self.get_logger().info(f'Iniciando desenho de {len(points)} pontos...')
            time.sleep(1.0)

            # Levanta caneta e move para primeiro ponto
            self.set_pen(off=1)
            self.teleport_turtle(points[0][0], points[0][1])
            self.set_pen(off=0)

            # Desenha todos os pontos
            jump_threshold = 0.3  # Limiar de distância para pular (levantando caneta)

            for i, (x, y) in enumerate(points):
                if i > 0:
                    # Verifica distância para ponto anterior
                    prev_x, prev_y = points[i - 1]
                    distance = np.sqrt((x - prev_x)**2 + (y - prev_y)**2)

                    if distance > jump_threshold:
                        # Pula: levanta caneta, teleporta, abaixa caneta
                        self.set_pen(off=1)
                        self.teleport_turtle(x, y)
                        self.set_pen(off=0)
                    else:
                        # Continua desenhando
                        self.teleport_turtle(x, y)

                if (i + 1) % 100 == 0:
                    self.get_logger().info(f'Desenhados {i + 1}/{len(points)} pontos')

            self.get_logger().info('Desenho completo!')
            return True

        except Exception as e:
            self.get_logger().error(f'Erro: {str(e)}')
            import traceback
            traceback.print_exc()
            return False


def main(args=None):
    rclpy.init(args=args)

    parser = argparse.ArgumentParser(description='Turtle Draw - Draw image with turtlesim')
    parser.add_argument('image', nargs='?', help='Path to image file')
    args = parser.parse_args(args)

    if args.image is None:
        print('Usage: turtle_drawer <image_path>')
        print('Example: turtle_drawer /path/to/image.png')
        return

    node = TurtleDrawer(image_path=args.image)

    try:
        node.draw_image()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
