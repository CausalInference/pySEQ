import itertools
import matplotlib.pyplot as plt
import polars as pl

def _survival_plot(self):
    plt.figure(figsize=(10, 6))
    
    if self.plot_type == "risk":
        plot_data = self.km_data.filter(pl.col("estimate") == "risk")
    else: 
        plot_data = self.km_data.filter(pl.col("estimate") == "survival")
    
    color_cycle = None
    if self.plot_colors:
        color_cycle = itertools.cycle(self.plot_colors) 
        
    for idx, i in enumerate(self.treatment_level):
        subset = plot_data.filter(pl.col(self.treatment_col) == i)
        if subset.is_empty():
            continue
        label = f"treatment = {i}"
        if self.plot_labels and idx < len(self.plot_labels):
            label = self.plot_labels[idx]
        
        color = None
        if color_cycle:
            color = next(color_cycle)
        
        line, = plt.plot(
            subset["followup"], 
            subset["pred"], 
            "-",
            label=label,
            color=color
        )
        
        line_color = line.get_color() 
        
        if 'LCI' in subset.columns and 'UCI' in subset.columns:
            plt.fill_between(
                subset["followup"],
                subset["LCI"],
                subset["UCI"],
                color=line_color,
                alpha=0.2,
                label='_nolegend_'
            )
    if self.plot_title is None:
        self.plot_title = f"Cumulative {self.plot_type.title()}"
    
    plt.xlabel("Followup")
    plt.ylabel(self.plot_type.title())
    plt.title(self.plot_title)
    plt.legend()
    plt.grid()
    plt.show()