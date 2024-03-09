from tkinter import *
from PIL import Image, ImageGrab
import os

class Container:

    def __init__(self, width, height, frame_rate=5, gif_path=None, gif_length=100):
        """
        Create a container to draw on.

        Parameters
        ----------
        width : int
            The width of the container.
        height : int
            The height of the container.
        frame_rate : int, optional
            The frame rate of the container. Default is 5.
        gif_path : str, optional
            The path to save the container as a gif. Default is None.
        gif_length : int, optional
            The number of frames of the gif. Default is 100.
        """
        self.width = width
        self.height = height
        self.frame_rate = frame_rate

        if gif_path:
            self.gif_path = gif_path
            self.gif_length = gif_length
            self.gif_frames = []

            if os.path.exists(gif_path):
                os.remove(gif_path)

        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.setup()

        def _draw():
            self.canvas.delete("all")
            self.draw()

            if gif_path and len(self.gif_frames) < self.gif_length:
                self.gif_frames.append(self.capture_frame())

                if len(self.gif_frames) == self.gif_length:
                    self.gif_frames[1].save(
                        self.gif_path,
                        save_all=True,
                        append_images=self.gif_frames[1:],
                        duration=100,
                        loop=0
                    )
            self.root.after(int(1000 / self.frame_rate), _draw)
        self.root.after(0, _draw)

        def _shutdown():
            self.shutdown()
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", _shutdown)
        
        self.root.mainloop()

    def setup(self):
        """Override this method to setup the container before the main loop."""
        pass

    def draw(self):
        """Override this method to draw on the canvas."""
        pass

    def shutdown(self):
        """Override this method to perform actions before the window is closed."""
        pass

    def bind(self, event, callback):
        """
        Bind an event to a callback.
        
        Parameters
        ----------
        event : str
            The event to bind. For example, "<Button-1>" for left click.
        callback : function
            The function to call when the event is triggered.

        Example
        -------
        To bind a function to the left click event:

        >>> def left_click(event):
        >>>     print("Left click at", event.x, event.y)
        >>> container = Container(500, 500)
        >>> container.bind("<Button-1>", left_click)
        """
        self.root.bind(event, callback)

    def draw_grid(self, cols, rows, cell_size, color="light gray", linewidth=1):
        """
        Draw a grid on the canvas.

        Parameters
        ----------
        cols : int
            The number of columns.
        rows : int
            The number of rows.
        cell_size : int, tupel(int, int)
            The size of each cell.
        color : str, optional
            The color of the grid. Default is "light gray".
        linewidth : int, optional
            The width of the grid lines. Default is 1.
        """
        if type(cell_size) == int:
            cell_size = (cell_size, cell_size)

        for i in range(cols + 1):
            # Draw vertical lines
            self.canvas.create_line(i * cell_size[0], 0,
                                    i * cell_size[0], rows * cell_size[1],
                                    fill=color, width=linewidth)
        for j in range(rows + 1):
            # Draw horizontal lines
            self.canvas.create_line(0, j * cell_size[1],
                                    cols * cell_size[0], j * cell_size[1],
                                    fill=color, width=linewidth)
            
    def capture_frame(self):
        """
        Capture the current frame of the canvas.

        Returns
        -------
        Image
            The current frame of the canvas.
        """
        x0 = self.root.winfo_rootx() 
        y0 = self.root.winfo_rooty()
        x1 = x0 + self.root.winfo_width()
        y1 = y0 + self.root.winfo_height()

        return ImageGrab.grab(xdisplay=":0").crop((x0, y0, x1, y1))
