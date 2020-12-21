from tkinter import PhotoImage


class Laser:        #create the laser object and its according properties and values
    def __init__(self, canvas, x = 0, y = 0):
        self.__canvas = canvas
        self.__imgLaser = PhotoImage(file="images/laserbeam.png")
        self.__xpos = x
        self.__ypos = y
        self.__laser = self.__canvas.create_image(self.__xpos, self.__ypos, image=self.__imgLaser)
        self.__width = self.__imgLaser.width()
        self.__height = self.__imgLaser.height()

        self.__shootTimer = None

    def shoot(self):        #animate the laser
        self.__shootTimer = self.__canvas.after(3, self.shoot)
        self.__xpos += 6
        self.__canvas.coords(self.__laser, self.__xpos, self.__ypos)

        if self.__xpos >= self.__canvas.winfo_reqwidth():
            self.deleteLaser()

    def getLeftSide(self):
        """
        Returns the x position of the left side of the laser

        RETURNS:
        --------
        int
            The x position of the left side of the laser
        """
        return self.__xpos

    def getTopSide(self):
        """
        Returns the y position of the top side of the laser

        RETURNS:
        --------
        int
            The y position of the top side of the laser
        """
        return self.__ypos

    def getRightSide(self):
        """
        Returns the x position of the right side of the laser

        RETURNS:
        --------
        int
            The x position of the right side of the laser
        """
        return self.__xpos + self.__width

    def getBottomSide(self):
        """
        Returns the y position of the bottom side of the laser

        RETURNS:
        int
            The y position of the bottom side of the laser
        """
        return self.__ypos + self.__height

    def deleteLaser(self):      #delete(hide) the laser
        self.__xpos, self.__ypos = 0, 0
        self.__canvas.coords(self.__laser, self.__xpos, self.__ypos)
        self.__canvas.after_cancel(self.__shootTimer)
        self.__imgLaser = None
