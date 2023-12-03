import numpy as np
import cv2


class gradientItem:
    def __init__(self, color, position) -> None:
        self.color = color
        self.position = position
        self.absolute_pos = -1

    def calc_absolute_pos(self, size):
        self.absolute_pos = int(self.position * size)


class colorGradient:
    def __init__(self) -> None:
        self.colors = []
        self.gradiant = None

    def add_color(self, color, position):
        self.colors.append(gradientItem(color, position))

    def reset(self):
        self.colors = []

    def generate_gradiant(self, size, smooth=True):


        self.colors.sort(key=lambda x: x.position)

        # if fisrt color start from mid:
        if self.colors[0].position > 0:
            self.colors.insert(0, gradientItem(self.colors[0].color, 0))

        if self.colors[-1].position < 1:
            self.colors.append(gradientItem(self.colors[-1].color, 1))

        self.gradiant = np.zeros((1, size, 3), dtype=np.uint8)

        for c_idx in range(len(self.colors) - 1):
            # ------------
            item1 = self.colors[c_idx]
            item2 = self.colors[c_idx + 1]
            item1.calc_absolute_pos(size)
            item2.calc_absolute_pos(size)
            # ------------
            for channle in range(3):
                ch = np.linspace(
                    item1.color[channle],
                    item2.color[channle],
                    item2.absolute_pos - item1.absolute_pos,
                    dtype=np.uint8,
                )
                self.gradiant[0, item1.absolute_pos : item2.absolute_pos, channle] = ch

        # ---------------- fill start

        if smooth:
            self.gradiant = cv2.blur(self.gradiant, ksize=(int(size / 10), 1))
        return self.gradiant

    def toImage(self, width):
        _, h, _ = self.gradiant.shape
        image = np.zeros((h, width, 3), dtype=np.uint8)
        for i in range(width):
            image[:, i, :] = self.gradiant
        return image

G10= colorGradient()

G10.add_color((0, 0, 255), 0)
G10.add_color((0, 255, 255), .22)
G10.add_color((255, 0, 0), .33)
G10.add_color((0, 0, 0), .44)
G10.add_color((0, 0, 0),.55)  # white clack


if __name__ == "__main__":
    cg = colorGradient()
    cg.add_color((255, 0, 0), 0)
    cg.add_color((255, 255, 0), 0.3)
    cg.add_color((0, 255, 0), 0.5)
    cg.add_color((0, 255, 255), 0.7)
    cg.add_color((0, 0, 255), 1)
    gradiant = cg.generate_gradiant(500)
    img = cg.toImage(200)

    cv2.imshow("grad", img)
    cv2.waitKey(0)
