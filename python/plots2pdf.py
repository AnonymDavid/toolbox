import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np
from glob import glob
import os
from typing import List, Tuple


def plots2pdf(root:str,
            x_headers:List[str],
            y_headers:List[str],
            x_axis_label:str,
            y_axis_label:str,
            x_limits:Tuple[float,float]=(0,0),
            y_limits:Tuple[float,float]=(0,0),
            plots_in_page:Tuple[int,int]=(3,1),
            plot_labels:List[str]=[],
            output_dir:str='plot',
            legend=True,
            grid:bool=True,
            tight_layout:bool=True,
            sort_by_name=True,
            recursive=True,
            verbose=True) -> None:
    """
    Convert CSV files to a PDF containing plots.

    Args:
        root (str): The root directory where the CSV files are located.
        x_headers (List[str]): The list of column headers to be used as the x-axis data for the plots.
        y_headers (List[str]): The list of column headers to be used as the y-axis data for the plots.
        x_axis_label (str): The label for the x-axis.
        y_axis_label (str): The label for the y-axis.
        x_limits (Tuple[float,float], optional): The limits for the x-axis. Leave at (0,0) to auto adjust. Defaults to (0,0).
        y_limits (Tuple[float,float], optional): The limits for the y-axis. Leave at (0,0) to auto adjust. Defaults to (0,0).
        plots_in_page (Tuple[int,int], optional): The number of plots to be displayed in each page (row, column). Defaults to (3,1).
        plot_labels (List[str], optional): The labels for each plot. Defaults to x and y data headers.
        output_dir (str, optional): The directory where the PDF file will be saved relative to root. Defaults to 'plot'.
        legend (bool, optional): Whether to display the legend on the plots. Defaults to True.
        grid (bool, optional): Whether to display grid lines on the plots. Defaults to True.
        tight_layout (bool, optional): Whether to adjust the plot with smaller margins. Defaults to True.
        sort_by_name (bool, optional): Whether to sort the CSV files by name. Defaults to True.
        recursive (bool, optional): Whether to search for CSV files recursively in subdirectories. Defaults to True.
        verbose (bool, optional): Whether to print progress information. Defaults to True.

    Returns:
        None
    """

    if not os.path.isdir(root):
        raise ValueError('Invalid root directory.')

    if not isinstance(x_headers, list) or not isinstance(y_headers, list):
        raise ValueError('x_headers and y_headers must be lists.')

    if len(x_headers) != len(y_headers) or len(x_headers) != len(plot_labels):
        raise ValueError('x_headers, y_headers, and plot_labels must have the same length.')

    if not isinstance(x_axis_label, str) or not isinstance(y_axis_label, str):
        raise ValueError('x_axis_label and y_axis_label must be strings.')

    if not isinstance(plots_in_page, tuple) or len(plots_in_page) != 2:
        raise ValueError('plots_in_page must be a tuple of length 2.')
    
    if plots_in_page[0] < 1 or plots_in_page[1] < 1:
        raise ValueError('plots_in_page must have non-zero positive integer values.')

    if not isinstance(plot_labels, list):
        raise ValueError('plot_labels must be a list.')

    if not isinstance(grid, bool) or not isinstance(tight_layout, bool) or not isinstance(sort_by_name, bool) or not isinstance(recursive, bool) or not isinstance(verbose, bool):
        raise ValueError('grid, tight_layout, sort_by_name, recursive, and verbose must be booleans.')
    

    files = glob(f'{root}{"/**" if recursive else ""}/*.csv', recursive=recursive)

    if not os.path.exists(f'{root}/{output_dir}/'):
        os.mkdir(f'{root}/{output_dir}/')

    if sort_by_name:
        files.sort()

    current_plot = 1
    file_counter = 0
    file_count = len(files)

    rownum = plots_in_page[0]
    colnum = plots_in_page[1]

    fig = plt.figure(figsize=(8.3, 11.7))

    with PdfPages(f'{root}/{output_dir}/output.pdf') as pdf:
        for input in files:
            df = pd.read_csv(input)

            sub = fig.add_subplot(rownum, colnum, current_plot, xlabel=x_axis_label, ylabel=y_axis_label)
            sub.set_title(os.path.splitext(os.path.basename(input))[0])

            for i in range(len(x_headers)):
                x = np.array(df[x_headers[i]])
                y = np.array(df[y_headers[i]])

                sub.plot(x, y, label=(plot_labels[i] if plot_labels else f'{x_headers[i]} - {y_headers[i]}'))

            if x_limits[0] != 0 or x_limits[1] != 0:
                sub.set_xlim(x_limits)

            if y_limits[0] != 0 or y_limits[1] != 0:
                sub.set_ylim(y_limits)

            if grid:
                sub.grid(linestyle='dashed', linewidth=0.5, alpha=1, dashes=(1,10,1,10))

            if legend:
                sub.legend()

            if verbose:
                print(f'{file_counter+1}/{file_count}\t{os.path.split(input)[1][:-4]}')
                
            file_counter += 1
            current_plot += 1

            if current_plot > rownum*colnum:
                if tight_layout:
                    fig.tight_layout()
                pdf.savefig(fig)
                fig.clf()
                current_plot = 1
