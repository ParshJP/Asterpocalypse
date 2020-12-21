from tkinter import PhotoImage

class Asteroid:     #create an asteroid object and its according properties and values
    def __init__(self, canvas, size=1, x = 1004, y=283, speed=1):
        self.__canvas = canvas
        self.__imgAsteroids = [PhotoImage(file="images/asteroid0.png"),
                               PhotoImage(file="images/asteroid1.png"),
                               PhotoImage(file="images/asteroid2.png")]
        self.__imgExplosions = [PhotoImage(file="images/explosion0.png"),
                                PhotoImage(file="images/explosion1.png"),
                                PhotoImage(file="images/explosion2.png")]

        self.__size = size

        self.__currentImgAsteroid = self.__imgAsteroids[size]
        self.__currentImgExplosion = self.__imgExplosions[size]

        self.__speed = speed

        self.__width = self.__currentImgAsteroid.width()
        self.__height = self.__currentImgAsteroid.height()

        self.__xpos = x
        self.__ypos = y

        self.__asteroid = self.__canvas.create_image(self.__xpos, self.__ypos, image=self.__currentImgAsteroid,
                                                     anchor="nw")

        self.__timer = None

        self.__hits = 0

    def move(self):     #animate the asteroid
        self.__timer = self.__canvas.after(10, self.move)
        self.__xpos -= self.__speed
        self.__canvas.coords(self.__asteroid, self.__xpos, self.__ypos)

    def getLeftSide(self):
        """
        Returns the x position of the left side of the asteroid

        RETURNS:
        --------
        int
            The x position of the left side of the asteroid
        """
        return self.__xpos

    def getTopSide(self):
        """
        Returns the y position of the top side of the asteroid

        RETURNS:
        --------
        int
            The y position of the top side of the asteroid
        """
        return self.__ypos

    def getRightSide(self):
        """
        Returns the x position of the right side of the asteroid

        RETURNS:
        --------
        int
            The x position of the right side of the asteroid
        """
        return self.__xpos + self.__width

    def getBottomSide(self):
        """
        Returns the y position of the bottom side of the asteroid

        RETURNS:
        --------
        int
            The y position of the bottom side of the asteroid
        """
        return self.__ypos + self.__height

    def getWidth(self):
        """
        Returns the width of the asteroid in pixels

        RETURNS:
        --------
        int
            The width of the asteroid in pixels
        """
        return self.__width

    def getHeight(self):
        """
        Returns the height of the asteroid in pixels

        RETURNS:
        --------
        int
            The height of the asteroid in pixels
        """
        return self.__height

    def getSize(self):
        """
        Returns the size classification of the asteroid

        RETURNS:
        --------
        int
            The size of the asteroid
        """
        return self.__size

    def getHits(self):
        """
        Returns the amount of times the asteroid has been shot

        RETURNS:
        --------
        int
            The amount shots the asteroid has taken
        """
        return self.__hits

    def getImg(self):
        """
        Returns a boolean value to signify the image of the asteroid

        RETURNS:
        --------
        bool
            Value to signify if img is asteroid or explosion
        """
        if self.__currentImgAsteroid == self.__imgAsteroids[self.__size]:
            return 0
        else:
            return 1

    def setImage(self):
        """
        Set the image of the asteroid to an explosion
        """
        self.__currentImgAsteroid = self.__currentImgExplosion
        self.__canvas.itemconfig(self.__asteroid, image = self.__currentImgAsteroid)

    def setSpeed(self, speed):
        """
        Set the speed of the asteroids moving across the screen.

        PARAMETERS:
        -----------
        int
            The number of pixels the asteroid moves to the left every 10 milliseconds
        """
        self.__speed = speed

    def setHits(self, hits):
        """
        Set the amount of times an asteroid has been hit

        PARAMETERS:
        -----------
        int
            The number of times the asteroid has been hit
        """
        self.__hits = hits

    def deleteAsteroid(self):           #delete(hide) the asteroid
        self.__xpos, self.__ypos = 1004, 600
        self.__canvas.coords(self.__asteroid, self.__xpos, self.__ypos)
        if self.__timer is not None:
            self.__canvas.after_cancel(self.__timer)
            self.__timer = None
