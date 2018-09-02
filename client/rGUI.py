from guizero import App, Box, Text, Picture

def run_Self():

    def updateCountDownText():
        print("func rGUI")
        # imgBox1.destroy()
        # imgBox1 = Picture(box1, image="qrcode.bmp")
        # imgBox1.value("qrcode.bmp")
        countDownText.after(1000, updateCountDownText)

    app = App(title="Seeed interactive camera demo on raspberry pi",
              width=1280,
              height=768,
              bg="black",
              layout="auto")
    app.tk.attributes("-fullscreen", True)
    box1 = Box(app, layout="auto", grid=[0, 0])
    rabbit1 = Text(box1, text="#", size=100, color="black")
    #
    # imgBox1 = Picture(app, image="qrcode.bmp")

    countDownText = Text(box1, text="请领取二维码小票", size=100, color="white")
    rabbit2 = Text(box1, text="#", size=70, color="black")
    warningText = Text(box1, text="或站到拍照点开始新一轮拍照", size=50, color="white")


    countDownText.after(1000, updateCountDownText)
    app.display()

    def hide_self():
        app.visible = False

    def show_self():
        app.visible = True

def read_input(visible_flag):
    return visible_flag

if __name__ == "__main__":
    run_Self()


