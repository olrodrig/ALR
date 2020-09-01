import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def plot_outliers(ax, axr, ALR):
    
  if ALR.with_y_errors:  
      x_out, y_out, err_y_out = ALR.x_outliers, ALR.y_outliers, ALR.err_y_outliers
  else:
      x_out, y_out = ALR.x_outliers, ALR.y_outliers

  ax.plot(x_out, y_out, 'or',markeredgecolor='k', zorder=2, label='outliers ('+str(len(x_out))+')')
  residuals_out = y_out - ALR.interp(x_out)[0]
  axr.plot(x_out, residuals_out, 'or',markeredgecolor='k')


def plot_sigma_limits(ax, x, y, err_y, lw=1, zorder=1, labels=False):
    
  if labels == True:
      ax.plot(x, y-1.0*err_y, '--', color='lime'  , lw=lw, zorder=zorder, label='1$\sigma$ limit')
      ax.plot(x, y-3.0*err_y, '--', color='orange', lw=lw, zorder=zorder, label='3$\sigma$ limit')
  else:
      ax.plot(x, y-1.0*err_y, '--', color='lime'  , lw=lw, zorder=zorder)
      ax.plot(x, y-3.0*err_y, '--', color='orange', lw=lw, zorder=zorder)
  ax.plot(x, y+1.0*err_y, '--', color='lime'  , lw=lw, zorder=zorder)
  ax.plot(x, y+3.0*err_y, '--', color='orange', lw=lw, zorder=zorder)
  
def set_ticks(ax, ax_ref):
    
  x_majors = ax_ref.xaxis.get_majorticklocs()
  x_minor  = ((max(x_majors) - min(x_majors)) / float(len(x_majors)-1))/5.0  
  ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(base=x_minor)) 
  
  y_majors = ax_ref.yaxis.get_majorticklocs()
  y_minor  =  ((max(y_majors) - min(y_majors)) / float(len(y_majors)-1))/4.0  
  ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(base=y_minor))
  
  ax.tick_params('both', length=6, width=1, which='major', direction='in')
  ax.tick_params('both', length=3, width=1, which='minor', direction='in')
  ax.xaxis.set_ticks_position('both')
  ax.yaxis.set_ticks_position('both')
    
#plot the input data and the loess fit, along with the residuals
def plot_ALR(ALRs, comparison_func=[], invert_y_axis=False, object_name='input data', xlabel='x', ylabel='y', figure_name=''):

  mpl.rcParams['legend.handlelength'] = 1.5
  plt.rc('axes', labelsize=12.5)
  plt.rc('xtick', labelsize=12.5)
  plt.rc('ytick', labelsize=12.5)
  plt.rc('legend', fontsize=12.5)
  
  axs, axrs = [], []
  xminmax, yminmax, rminmax = [], [], []
  if len(ALRs) == 1:
      fig = plt.figure(figsize=(8, 8))
      fig.subplots_adjust(left=0.105, bottom=0.057, hspace=0.01, right=1.00-0.01, top=0.92)
      axs.append(fig.add_subplot(211))
      axrs.append(fig.add_subplot(212))
  if len(ALRs) == 2:
      fig = plt.figure(figsize=(12, 8))
      fig.subplots_adjust(left=0.105*8.0/12.0, bottom=0.057, hspace=0.01, right=1.00-0.01*8.0/12.0, top=0.92, wspace=0.01)
      axs.append(fig.add_subplot(221))
      axrs.append(fig.add_subplot(223))
      axs.append(fig.add_subplot(222))
      axrs.append(fig.add_subplot(224))
  if len(ALRs) == 3:
      fig = plt.figure(figsize=(14, 8))
      fig.subplots_adjust(left=0.105*8.0/14.0, bottom=0.057, hspace=0.01, right=1.00-0.01*8.0/14.0, top=0.92, wspace=0.01*12.0/14.0)
      axs.append(fig.add_subplot(231))
      axrs.append(fig.add_subplot(234))
      axs.append(fig.add_subplot(232))
      axrs.append(fig.add_subplot(235))
      axs.append(fig.add_subplot(233))
      axrs.append(fig.add_subplot(236))
      
  for i in range(0, len(ALRs)):
      
      ALR = ALRs[i]
      ax, axr = axs[i], axrs[i]
      
      x             = ALR.x
      y             = ALR.y
      err_y         = ALR.err_y
      with_y_errors = ALR.with_y_errors
      N_data        = ALR.n_data
      N_fit         = ALR.n_fit
      N_outliers    = ALR.n_outliers
      alpha         = ALR.alpha
      deg           = ALR.deg
      outliers_det  = ALR.outliers_det
      
      
      #ALR fit
      x_ALR, y_ALR, err_y_ALR = ALR.x_ALR, ALR.y_ALR, ALR.err_y_ALR
      
      #plot input data
      if with_y_errors:  ax.plot([x,x], [y-err_y, y+err_y], '-', color='gray', zorder=1)
      ax.plot(x, y, 'o', color='white',markeredgecolor='k', zorder=2, label=object_name+' ('+str(N_data)+')')
      
      #plot comparison functions
      if len(comparison_func) != 0:
          
          plots, labels = [], []
          for func in comparison_func:
              
              y_for_res     = func['y'][func['x']>=min(x_ALR)]
              if 'err_y' in func.keys():  err_y_for_res = func['err_y'][func['x']>=min(x_ALR)]
              x_res         = func['x'][func['x']>=min(x_ALR)]
              
              y_for_res     = y_for_res[x_res<=max(x_ALR)]
              if 'err_y' in func.keys():  err_y_for_res = err_y_for_res[x_res<=max(x_ALR)]
              x_res         = x_res[x_res<=max(x_ALR)]
              
              res = y_for_res - np.interp(x_res, x_ALR, y_ALR)
              
              plot_func       , = ax.plot(func['x'], func['y'], '-' , color=func['color'], zorder=3, lw=2)
              axr.plot(x_res, res, '-', color=func['color'], zorder=3, lw=2)
              plots.append(plot_func)
              labels.append(func['label'])
              if 'err_y' in func.keys():
                  plot_func_3sigma, = ax.plot(func['x'], func['y']-3.0*func['err_y'], '--' , color=func['color'], zorder=2, lw=2)
                  ax.plot(func['x'], func['y']+3.0*func['err_y'], '--' , color=func['color'], zorder=2, lw=2)
                  axr.plot(func['x'], res-3.0*func['err_y'], '--', color=func['color'], zorder=3)
                  axr.plot(func['x'], res+3.0*func['err_y'], '--', color=func['color'], zorder=3)
                  plots.append(plot_func_3sigma)
                  labels.append('3$\sigma$ limit')
          leg2 = ax.legend(plots, labels, loc='best')
      
      #label for ALR
      if alpha != 0:
          if outliers_det == True:
              if N_outliers != 0:
                  label_text = r'ALR(N='+str(N_fit)+'; alpha='+str(round(alpha,3))+')'
                  if deg == 1: label_text = r'ALR(N='+str(N_fit)+'; alpha='+str(round(alpha,3))+'; deg='+str(deg)+')'
              else:
                  label_text = r'ALR(N='+str(N_fit)+'; alpha='+str(round(alpha,3))+'; outliers_det=True)'
                  if deg == 1: label_text = r'ALR(N='+str(N_fit)+'; alpha='+str(round(alpha,3))+'; deg='+str(deg)+'; outliers_det=True)'
          else:
              if len(ALRs) == 3:
                  label_text = r'ALR('+str(N_fit)+r'; $\alpha$='+str(round(alpha,3))+'; outliers_det=F)'
                  if deg == 1: label_text = r'ALR('+str(N_fit)+r'; $\alpha$='+str(round(alpha,3))+'; deg='+str(deg)+'; outliers_det=F)'
              else:
                  label_text = r'ALR(N='+str(N_fit)+'; alpha='+str(round(alpha,3))+'; outliers_det=False)'
                  if deg == 1: label_text = r'ALR(N='+str(N_fit)+'; alpha='+str(round(alpha,3))+'; deg='+str(deg)+'; outliers_det=False)'
      else:
          label_text = 'linear intpol between points'
          
      #plot ALR fit
      ax.plot(x_ALR, y_ALR, '-', color='b', zorder=4, lw=2, label=label_text)
      plot_sigma_limits(ax, x_ALR, y_ALR, err_y_ALR, lw=1, zorder=1, labels=True)
      
      #residuals
      axr.plot([min(x), max(x)], [0.0, 0.0], '--k')
      residuals = y - ALR.interp(x)[0]
      
      #plot residuals
      if with_y_errors:  axr.plot([x,x], [residuals-err_y, residuals+err_y], '-', color='gray', zorder=1)
      axr.plot(x, residuals, 'ok', color='white',markeredgecolor='k', zorder=2)
      plot_sigma_limits(axr, x_ALR, 0.0, err_y_ALR, lw=2, zorder=3, labels=False)
        
      #outliers
      if N_outliers != 0:  plot_outliers(ax, axr, ALR)

      if N_outliers == 0:
          ax.legend(bbox_to_anchor=(0.0, 1.085, 1.0, 0.10),loc='best', ncol=2, borderaxespad=0., handletextpad=0.2, mode='expand', numpoints=1)
      else:
          ax.legend(bbox_to_anchor=(0.0, 1.085, 1.0, 0.10),loc='best', ncol=3, borderaxespad=0., handletextpad=0.2, mode='expand', numpoints=1)
      if len(comparison_func) != 0: ax.add_artist(leg2)
      if i == 0:
          ax.set_ylabel(ylabel)
          axr.set_ylabel('residuals')
      axr.set_xlabel(xlabel)      
      
      #limits
      x_for_limits, y_for_limits, err_y_for_limits = x, y, err_y
      r_for_limits, err_y_ALR_for_limits = residuals, err_y_ALR
      
      xmin, xmax = min(x_for_limits), max(x_for_limits)
      if i == len(ALRs)-1:  xminmax.extend([xmin, xmax])
      
      if hasattr(err_y, '__len__') == True:
          ymin, ymax = min(y_for_limits-err_y_for_limits), max(y_for_limits+err_y_for_limits)
      else:
          ymin, ymax = min(y_for_limits), max(y_for_limits)
      if i == len(ALRs)-1:  yminmax.extend([ymin, ymax])    
      
      if hasattr(err_y, '__len__') == True:
          rmin, rmax = min([min(-3.0*err_y_ALR_for_limits),min(r_for_limits-err_y_for_limits)]), max([max(3.0*err_y_ALR_for_limits), max(r_for_limits+err_y_for_limits)])
      else:
          rmin, rmax = min([min(-3.0*err_y_ALR_for_limits),min(r_for_limits)]), max([max(3.0*err_y_ALR_for_limits), max(r_for_limits)])
      if i == len(ALRs)-1:  rminmax.extend([rmin, rmax])
      
      ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
      if i != 0: 
          ax.yaxis.set_major_formatter(mpl.ticker.NullFormatter())
          axr.yaxis.set_major_formatter(mpl.ticker.NullFormatter())
      
      
  xmin, xmax = min(xminmax), max(xminmax)
  dx = (xmax-xmin)*0.025
  ymin, ymax = min(yminmax), max(yminmax)
  dy = (ymax-ymin)*0.05
  rmin, rmax = min(rminmax), max(rminmax)
  dr = (rmax-rmin)*0.05
  
  for i in range(0, len(ALRs)):
      axs[i].set_xlim(xmin-dx, xmax+dx)
      axrs[i].set_xlim(xmin-dx, xmax+dx)
      axs[i].set_ylim(ymin-dy, ymax+dy)
      axrs[i].set_ylim(rmin-dr, rmax+dr)
      set_ticks(axs[i],axs[len(ALRs)-1])
      set_ticks(axrs[i],axrs[len(ALRs)-1])
      if invert_y_axis == True:
          axs[i].invert_yaxis()
          axrs[i].invert_yaxis()
  
  if figure_name != '':  fig.savefig(figure_name+'.pdf', dpi=100)
