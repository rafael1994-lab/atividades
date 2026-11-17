import pyautogui
import csv
import time

time.sleep(2)

time.sleep(2)
        pyautogui.click(234,138, duration=2)
        pyautogui.write(produto["codigo"])

with open(r"C:\Users\1079588\Documents\UC13\atividades\input\dia05novembro\produtos.csv",
    "r",
    encoding="utf-8-sig",) as arquivo:
    leitor = csv.DictReader(arquivo)
    for produto in leitor:
        time.sleep(2)
        pyautogui.click(113,201, duration=2)
        pyautogui.write(produto["codigo"])

        time.sleep(2)
        pyautogui.click(230,200, duration=2)
        pyautogui.write(produto["nome"])

        time.sleep(2)
        pyautogui.click(342,198, duration=2)
        pyautogui.write(produto["categoria"])

        time.sleep(2)
        pyautogui.click(450,200, duration=2)
        pyautogui.write(produto["preço"])

        time.sleep(2)
        pyautogui.click(559,200, duration=2)
        pyautogui.write(produto["quantidade"])

        time.sleep(2)
        pyautogui.click(327,614, duration=2)
        pyautogui.press("enter")

        time.sleep(2)
print("Cadastros realizado!!")