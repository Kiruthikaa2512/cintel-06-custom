from shiny.express import ui, input, output, render
from shiny import reactive
from shinywidgets import render_plotly
from plotly import graph_objs as go
import pandas as pd
import random
from pathlib import Path

# -------------------- Constants --------------------
UPDATE_INTERVAL_SECS = 25
CSV_PATH = Path(__file__).parent / "Inventory-Tracking.csv"

# -------------------- Load Initial Data --------------------
inventory_df = pd.read_csv(CSV_PATH)
supplier_choices = ["All"] + sorted(inventory_df["Supplier"].unique())

# -------------------- UI Layout --------------------
ui.page_opts(title="Inventory Monitor Dashboard by Kiruthikaa", fillable=True)

with ui.sidebar(open="open"):
    ui.input_select("supplier", "Filter by Supplier", choices=supplier_choices, selected="All")
    ui.input_slider("min_stock", "Minimum Quantity to Show", min=0, max=100, value=10)
    ui.hr()
    ui.markdown(f"Auto-refresh every {UPDATE_INTERVAL_SECS} seconds.")
   
    @output
    @render.ui
    def refresh_status():
        df = live_inventory()
        last_refresh = pd.Timestamp.now().strftime('%H:%M:%S')
        return ui.markdown(f"**Last refreshed at:** {last_refresh}")

# -------------------- Reactive Inventory Updates --------------------
@reactive.calc()
def live_inventory():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    df = inventory_df.copy()
    df["QuantityInStock"] = df["QuantityInStock"].apply(
        lambda x: max(0, x + random.randint(-3, 3))
    )
    return df

# -------------------- Filter Logic --------------------
@reactive.calc()
def filtered_inventory():
    df = live_inventory()
    if input.supplier() != "All":
        df = df[df["Supplier"] == input.supplier()]
    return df[df["QuantityInStock"] >= input.min_stock()]

# -------------------- Value Boxes --------------------
with ui.layout_columns():
    @output
    @render.ui
    def value_boxes():
        df = filtered_inventory()
        low_stock_count = df[df["QuantityInStock"] < df["ReorderPoint"]].shape[0]
        total_value = (df["QuantityInStock"] * df["UnitCost"]).sum()

        return ui.div(
            ui.value_box(value=str(len(df)), title="Filtered Products", showcase="📦"),
            ui.value_box(value=str(low_stock_count), title="Low Stock Items", showcase="⚠️"),
            ui.value_box(value=f"${total_value:,.2f}", title="Inventory Value", showcase="💰")
        )

    # -------------------- Inventory Table --------------------
    @output
    @render.data_frame
    def inventory_table():
        return render.DataGrid(filtered_inventory())

    # -------------------- Low Stock Bar Chart --------------------
    @output
    @render_plotly
    def low_stock_chart():
        df = filtered_inventory()
        low_df = df[df["QuantityInStock"] < df["ReorderPoint"]]

        fig = go.Figure(
            data=go.Bar(
                x=low_df["ProductName"],
                y=low_df["QuantityInStock"],
                marker_color="crimson"
            )
        )
        fig.update_layout(
            title="Low Stock Products",
            xaxis_title="Product",
            yaxis_title="Quantity in Stock"
        )
        return fig

    # -------------------- Supplier Value Donut Chart --------------------
    @output
    @render_plotly
    def supplier_value_chart():
        df = filtered_inventory()
        grouped = df.groupby("Supplier").apply(
            lambda g: (g["QuantityInStock"] * g["UnitCost"]).sum()
        ).reset_index(name="TotalValue")

        fig = go.Figure(
            data=go.Pie(
                labels=grouped["Supplier"],
                values=grouped["TotalValue"],
                hole=0.4,  # Donut shape
                textinfo="label+percent",
                hoverinfo="label+value"
            )
        )
        fig.update_layout(
            title="Inventory Value by Supplier (Donut Chart)",
            showlegend=True
        )
        return fig
