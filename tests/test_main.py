import unittest
import numpy as np
import cv2 as cv
from main import calculate_ear, divide_keys, draw_keyboard

class TestMainFunctions(unittest.TestCase):

    def test_divide_keys(self):
        keys = ['Q', 'W', 'E', 'R', 'T', 'Y']
        left, right = divide_keys(keys)
        # Verifica se a divisão está correta para uma lista par de teclas
        self.assertEqual(left, ['Q', 'W', 'E'])
        self.assertEqual(right, ['R', 'T', 'Y'])

        keys_odd = ['A', 'S', 'D', 'F', 'G']
        left, right = divide_keys(keys_odd)
        # Verifica se a divisão está correta para uma lista ímpar de teclas
        self.assertEqual(left, ['A', 'S'])
        self.assertEqual(right, ['D', 'F', 'G'])

    def test_draw_keyboard(self):
        # Cria uma imagem fictícia
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        left_keys = ['Q', 'W', 'E']
        right_keys = ['Y', 'U', 'I']
        selected_letters = ['A']

        # Chama a função draw_keyboard
        frame_with_keyboard = draw_keyboard(frame, left_keys, right_keys, selected_letters)
        
        # Verifica as dimensões da imagem aumentada
        self.assertEqual(frame_with_keyboard.shape[0], frame.shape[0] + 200 + 50)
        self.assertEqual(frame_with_keyboard.shape[1], frame.shape[1])

        # Verifica se a seleção de letras aparece na imagem
        text_position = (30, frame.shape[0] + 230)
        text_color = (0, 255, 0)
        # Usa o método de matching de template para verificar se o texto foi adicionado
        result = cv.matchTemplate(frame_with_keyboard, cv.putText(np.zeros_like(frame_with_keyboard), "Selected Letters: A", text_position, 
                                                                   cv.FONT_HERSHEY_SIMPLEX, 1, text_color, 2), cv.TM_CCOEFF)
        _, max_val, _, _ = cv.minMaxLoc(result)
        # Max_val deve ser alto se o texto estiver presente corretamente
        self.assertGreater(max_val, 1000000)  # Valor que representa uma correspondência confiável

if __name__ == "__main__":
    unittest.main()
