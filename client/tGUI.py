from guizero import App, Box, Text

input_countdownText = 5
input_warningText = "NONE"


def run_self():
    def updateCountDownText():
        countDownText.value = input_val()
        print("func tGUI")
        countDownText.after(1000, updateCountDownText)

    def input_val():
        global input_countdownText
        if input_countdownText == 0:
            input_countdownText = 5
            app.destroy()
            return -1
        input_countdownText = input_countdownText - 1
        if input_countdownText == 0:
            return "..."
        else:
            return input_countdownText

    app = App(title="Seeed interactive camera demo on raspberry pi",
              width=1280,
              height=768,
              bg="black",
              layout="auto")
    app.tk.attributes("-fullscreen", True)
    box1 = Box(app, layout="auto", grid=[0, 0])
    countDownText = Text(box1, text="5", size=400, color="white")
    warningText = Text(box1, text="拍照倒计时", size=70, color="white")
    countDownText.after(1000, updateCountDownText)
    app.display()
