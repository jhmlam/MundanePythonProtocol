# I will summarise the trick as follow:
# 1. Retrieve the matplotlib axes object 
# 2. Copy most axes atttributes (e.g. line data and legend) into a another axes
# 3. Plot by inverting the x and y

# An Example:
# "structurename" and "ionname" can be any string
# "granddf" is a pandas dataframe object with 2 columns "Z axis (nm)" and "PMF (kcal/mol)", which you may adapt to your own needs.

def CheckConvergence(structurename,ionname, granddf):


  local_granddf = granddf.loc[granddf['Ion'] == '%s' %(ionname)]
  sns.set_context("talk")

  # This is the axes object to be copied from
  ax = sns.lineplot(x="Z axis (nm)", y="PMF (kcal/mol)", data = local_granddf, hue = 'Analysis', ci = 90, palette = 'coolwarm_r')
  plt.legend(fontsize='xx-small', frameon=False, loc='upper left')
  legend_handles,legend_labels = ax.get_legend_handles_labels()

  # Create new axes
  fig_vert, (ax_vert, ax_dummy) = plt.subplots(ncols=2)

  # Copy axes attributes
  for u in range(len(ax.lines)):
      x,y =ax.lines[u].get_data()
      color_line = ax.lines[u].get_color()
      ax_vert.plot(y,x, color = color_line)

  for u in range(len(ax.collections)):
      c = ax.collections[u].get_paths()[0].vertices
      ax_vert.fill_between(c[:,1], c[:,0], alpha=0.5)
      
  ax_vert.set_xlabel(ax.get_xlabel())
  ax_vert.set_ylabel(ax.get_ylabel())
  
  # Clear the initial axes
  ax.clear()

  # Horizontal lines
  ax_vert.axhline(y= 1.3921, lw = 1.0, c = 'k', ls = '--')
  ax_vert.axhline(y=-1.2879, lw = 1.0, c = 'k', ls = '-')

  # Put legend in dummy
  ax_dummy.legend(legend_handles, legend_labels, fontsize='xx-small', frameon=False, loc='upper left')

  # Define limit and title
  ax_vert.set_xlim(left = 0.0, right = 5.5)
  ax_vert.set_ylim(bottom = -7.0, top = 7.0)
  ax_vert.title.set_text('%s' %(ionname))

  # Save figure
  plt.tight_layout()
  fig_vert.savefig("%s_%s_US_WHAM_Boot_Convergence_vert.png" %(structurename,ionname), dpi = 800)
  plt.clf()
