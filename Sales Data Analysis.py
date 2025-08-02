import pandas as pd
import numpy as np
import matplotlib

import matplotlib.pyplot as plt



def main():
    ds=load_dataset(input("Enter your file name : "))
    ds['Order Date'] = pd.to_datetime(ds['Order Date'], dayfirst=True, errors='coerce')
    ds['Ship Date'] = pd.to_datetime(ds['Ship Date'], dayfirst=True, errors='coerce')

    analys_sales_per_month(ds)
    get_product_sales(ds)

def analys_sales_per_month(ds):
    """Analyze and visualize monthly sales trends over time.

        Args:
            ds (DataFrame): Input dataset containing sales data
        """
    ds['Year'] = ds['Order Date'].dt.year
    ds['Month'] = ds['Order Date'].dt.month
    sales_pm_ds = ds.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
    sales_pm_ds['Date'] = pd.to_datetime(
        sales_pm_ds['Year'].astype(str) + '-' +
        sales_pm_ds['Month'].astype(str)
    )
    sales_pm_ds=sales_pm_ds.drop(["Month","Year"],axis=1)
    print("\n\n",sales_pm_ds)
    save_in_csv_file(sales_pm_ds,"Monthly_Sales_Over_Time.csv")
    plot_line(sales_pm_ds,"Date","Sales","Monthly Sales Over Time")

def get_product_sales(ds):
    """Analyze product sales performance and identify best/worst sellers.

        Args:
            ds (DataFrame): Input dataset containing product sales data
        """

    product_df = ds.groupby('Product Name')['Sales'].sum().reset_index()
    product_df.columns = ['Product Name', 'Sales']

    product_df = product_df.sort_values(by='Sales')

    print("Best product sales is : \n",product_df.iloc[-1])
    print("Worst product sales is : \n",product_df.iloc[0])
    save_in_csv_file(product_df,"Products_Sales.csv")



def load_dataset (file_path):
    """Load dataset from CSV file and perform initial data inspection.

        Args:
            file_path (str): Path to the CSV file

        Returns:
            DataFrame: Loaded dataset or None if file not found
        """
    try :
        ds=pd.read_csv(file_path)
        print("Missing Values : \n" ,ds.isnull().sum())
        print ("\nSummary state : \n",ds.describe())
        return ds
    except :
        TypeError("file isn't exist")
        return None


def plot_line(ds,x_name,y_name,title):
    """Generate and save a line plot from the given data.

      Args:
          ds (DataFrame): Data to plot
          x_name (str): Column name for x-axis
          y_name (str): Column name for y-axis
          title (str): Plot title
      """
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(ds[x_name], ds[y_name], marker='o')
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("Sales_Per_Month_Analys.png")
    plt.show()

def save_in_csv_file (df,file_name) :
    """Save DataFrame to CSV file.

       Args:
           df (DataFrame): Data to save
           file_name (str): Output file name
       """
    df.to_csv(file_name,index=False)

if __name__ == "__main__" :
    main()