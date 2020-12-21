from tkinter import PhotoImage


class Spaceship:          #create spaceship object and its according properties and values
    def __init__(self, canvas):
        self.__canvas = canvas
        self.__imgSpaceship = PhotoImage(file="images/spaceship.png")
        self.__imgExplosion = PhotoImage(file = 'images/exploded_ship.png')
        self.__width = self.__imgSpaceship.width()
        self.__height = self.__imgSpaceship.height()
        self.__xpos = 0
        self.__ypos = self.__canvas.winfo_reqheight() // 2 - self.__height // 2
        self.__spaceship = self.__canvas.create_image(self.__xpos, self.__ypos, image=self.__imgSpaceship, anchor="nw")

    def move(self, x, y):       #stop the spaceship from leaving the screen
        if 0 <= x <= self.__canvas.winfo_reqwidth() - self.__width - 5:
            self.__xpos = x
        if 60 <= y <= self.__canvas.winfo_reqheight() - self.__height - 5:
            self.__ypos = y
        self.__canvas.coords(self.__spaceship, self.__xpos, self.__ypos)

    def getLeftSide(self):
        """
        Returns the x position of the left side of the spaceship

        RETURNS:
        --------
        int
            The x position of the left side of the spaceship
        """
        return self.__xpos

    def getTopSide(self):
        """
        Returns the y position of the top side of the spaceship

        RETURNS:
        --------
        int
            The y position of the top side of the spaceship
        """
        return self.__ypos

    def getRightSide(self):
        """
        Returns the x position of the right side of the spaceship

        RETURNS:
        --------
        int
            The x position of the right side of the spaceship
        """
        return self.__xpos + self.__width

    def getBottomSide(self):
        """
        Returns the y position of the bottom of the spaceship

        RETURNS:
        --------
        int
            The y position of the bottom side of the spaceship
        """
        return self.__ypos + self.__height

    def getWidth(self):
        """
        Returns the width of the spaceship in pixels

        RETURNS:
        --------
        int
            The width of the spaceship in pixels
        """
        return self.__width

    def getHeight(self):
        """
        Returns the height of the spaceship in pixels

        RETURNS:
        --------
        int
            The height of the spaceship in pixels
        """
        return self.__height

    def getImg(self):
        """
        Returns a boolean value to signify the image of the spaceship

        RETURNS:
        --------
        bool
            Value to signify if img is ship or explosion
        """
        if self.__imgSpaceship == self.__imgExplosion:
            return 0
        else:
            return 1

    def setImage(self):
        """
        Set the image of the spaceship to an explosion
        """
        self.__imgSpaceship = self.__imgExplosion
        self.__canvas.itemconfig(self.__spaceship, image = self.__imgSpaceship)

    def deleteShip(self):       #delete(hide) the spaceship
        self.__xpos, self.__ypos = 0, 200
        self.__canvas.coords(self.__spaceship, self.__xpos, self.__ypos)
        self.__imgSpaceship = PhotoImage(file="images/spaceship.png")
        self.__canvas.itemconfig(self.__spaceship, image=self.__imgSpaceship)
