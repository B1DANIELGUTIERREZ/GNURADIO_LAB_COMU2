"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Promedios de tiempos',   # will show up in GRC
            in_sig=[np. float32 ],
            out_sig=[np. float32 ,np. float32 ,np. float32 ,np. float32 ,np. float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.acum_anterior = 0
        self.Ntotales = 0
        self.acum_anterior1 = 0
        self.acum_anterior2 = 0
        self.acum_anterior3 = 0

    def work(self, input_items, output_items):
        x = input_items[0] # Senial de entrada .
        y0 = output_items[0] # Promedio de la senial
        y1 = output_items[1] # Media de la senial
        y2 = output_items[2] # RMS de la senial
        y3 = output_items[3] # Potencia promedio de la senial
        y4 = output_items[4] # Desviacion estandar de la senial
        
        # Calculo de la media
        N = len (x)
        self.Ntotales = self.Ntotales + N
        acumulado = self.acum_anterior + np.cumsum(x)
        self.acum_anterior = acumulado[N-1]
        y0[:] = acumulado /self.Ntotales
        
        # Calculo de la media cuadratica
        x2=np.multiply(x,x)
        acumulado1 = self.acum_anterior1 + np.cumsum(x2)
        self.acum_anterior1 = acumulado[N-1]
        y1[:]=acumulado1/self.Ntotales
        
        # Calculo de la RMS
        x3=np.multiply(x,x)
        acumulado3 = self.acum_anterior3+ np.cumsum(x3)
        self.acum_anterior3 = acumulado3[N-1]
        y2[:] = np.sqrt(acumulado3 / self.Ntotales)
        
        # Calculo de la potencia promedio
        y3[:] = np.multiply (y2 ,y2)
        
        # Calculo de la desviacion estandar
        x1 = np.multiply (x-y0 ,x-y0)
        acumulado2 = self.acum_anterior2 + np.cumsum(x1)
        self.acum_anterior2 = acumulado2 [N -1]
        y4[:] = np.sqrt(acumulado2/self.Ntotales)
        
        

        return len(x)
