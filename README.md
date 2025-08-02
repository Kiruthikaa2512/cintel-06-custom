
```markdown
# Inventory Monitor Dashboard

A live-updating inventory monitoring dashboard built with Shiny for Python, Plotly, and Pandas. This interactive app visualizes stock levels, supplier distribution, and key metrics in real time.

---

## Features

- Live inventory simulation that refreshes every 25 seconds
- Filter products by supplier or minimum stock threshold
- Key performance indicators:
  - Filtered product count
  - Low stock alert count
  - Total inventory value
- Interactive charts:
  - Low stock bar chart
  - Supplier-based inventory value donut chart
- Interactive data table with filtering

---

## Project Structure

```

project-root/
├── dashboard/
│   └── app.py                   # Main Shiny application script
├── docs/
│   ├── Inventory-Tracking.csv   # Inventory data
│   ├── index.html               # Optional GitHub Pages landing page
│   └── screenshots/             # Optional UI screenshots
└── README.md                    # This file

````

---

## Requirements

Ensure Python 3.8+ is installed, then install required libraries:

```bash
pip install shiny shinywidgets pandas plotly faicons
````

---

## CSV Format

The dashboard reads data from `docs/Inventory-Tracking.csv`. The file must contain the following columns:

| Column          | Type    | Description                                           |
| --------------- | ------- | ----------------------------------------------------- |
| ProductName     | string  | Name of the product                                   |
| Supplier        | string  | Name of the supplier                                  |
| QuantityInStock | integer | Current inventory level                               |
| ReorderPoint    | integer | Threshold below which product is flagged as low stock |
| LeadTime        | float   | Lead time in days                                     |
| UnitCost        | float   | Cost per unit of the product                          |

### Example

Here is a sample of the CSV format:

```csv
ProductName,Supplier,QuantityInStock,ReorderPoint,LeadTime,UnitCost
Widget A,Supplier X,20,15,4,12.50
Widget B,Supplier Y,5,10,6,8.75
Widget C,Supplier X,40,25,3,15.00
Gadget A,Supplier Z,8,12,5,22.00
```

---

## Running the App Locally

1. Move to the dashboard directory:

```bash
cd dashboard
```

2. Launch the app using Shiny:

```bash
shiny run --reload app.py
```

3. Open the app in your browser (typically at `http://localhost:8000`).

---

## Deploying to ShinyApps.io

You can deploy the app to [ShinyApps.io](https://www.shinyapps.io/) using the following steps:

1. Sign up and log in to ShinyApps.io.
2. Install `rsconnect-python`:

```bash
pip install rsconnect-python
```

3. Authenticate your account (get the token from your ShinyApps dashboard):

```bash
rsconnect deploy shiny --name your-app-name --title "Inventory Monitor" app.py
```

4. Make sure the `Inventory-Tracking.csv` file is copied into the same folder (`dashboard/`) before deployment.

Refer to the [rsconnect-python documentation](https://github.com/posit-dev/rsconnect-python) for more details.

---

## Publishing on GitHub Pages

GitHub Pages only supports static content. Since Shiny apps require a running Python server, you **cannot run this app directly through GitHub Pages**.

However, the `docs/` folder can be used to host:

* Sample CSV files
* Static documentation
* Screenshots
* Landing pages that link to the live app (e.g., hosted on ShinyApps.io)

To enable GitHub Pages:

1. Go to your repository settings
2. Scroll to **Pages**
3. Set source to the `docs/` folder
4. Save the settings
---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it with attribution.

---

## Author

Built using [Shiny for Python](https://shiny.posit.co/py/)

```