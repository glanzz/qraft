import numpy as np
import matplotlib.pyplot as plt 

def generate_graph(XLABEL, YLABEL, XVALUES, BASELINEYVALUES, QRAFTYVALUES):
  # set width of bar 
  barWidth = 0.25
  fig = plt.subplots(figsize =(12, 8)) 
  
  # Set position of bar on X axis 
  br1 = np.arange(len(BASELINEYVALUES)) 
  br2 = [x + barWidth for x in br1] 

  
  # Make the plot
  plt.bar(br1, BASELINEYVALUES, color ='r', width = barWidth, 
          edgecolor ='grey', label ='Base') 
  plt.bar(br2, QRAFTYVALUES, color ='g', width = barWidth, 
          edgecolor ='grey', label ='QRAFT')
  
  # Adding Xticks 
  plt.xlabel(XLABEL, fontweight ='bold', fontsize = 15) 
  plt.ylabel(YLABEL, fontweight ='bold', fontsize = 15) 
  plt.xticks([r + barWidth for r in range(len(BASELINEYVALUES))], 
          XVALUES)
  
  plt.legend()
  plt.show()
