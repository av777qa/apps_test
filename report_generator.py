def generate_html_report(results, file_name="report.html"):
    rows = ""
    for r in results:
        color = "#d4edda" if r["status"] == "PASSED" else "#f8d7da"
        rows += f"""
        <tr style="background-color:{color}">
            <td>{r['device']}</td>
            <td>{r['version']}</td>
            <td>{r['status']}</td>
            <td>{r['reason']}</td>
        </tr>
        """
    html = f"""
    <html>
    <head>
        <title>Android/iOS Test Report</title>
        <style>
            body {{ font-family: Arial; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background-color: #333; color: white; }}
        </style>
    </head>
    <body>
        <h2>Android Devices Test Report</h2>
        <table>
            <tr>
                <th>Device</th>
                <th>Android Version</th>
                <th>Status</th>
                <th>Reason</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    with open(file_name, "w") as f:
        f.write(html)
