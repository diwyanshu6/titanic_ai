import matplotlib.pyplot as plt
import pandas as pd
import io
import base64


class VisualizationEngine:

    def __init__(self, df):
        self.df = df

    def is_visual_request(self, question: str):

        q = question.lower()

        keywords = [
            "show",
            "plot",
            "chart",
            "graph",
            "scatter",
            "visualize",
            "draw",
            "display"
        ]

        return any(k in q for k in keywords)

    def generate(self, question: str):

        q = question.lower()

        if "scatter" in q:
            plot_type = "scatter"
        elif "pie" in q:
            plot_type = "pie"
        elif "bar" in q:
            plot_type = "bar"
        else:
            plot_type = "hist"

        detected_columns = [
            col for col in self.df.columns
            if col.lower() in q
        ]

        if not detected_columns:
            return "Specify a valid column.", None

        fig = plt.figure()

        try:

            if plot_type == "scatter" and len(detected_columns) >= 2:
                x, y = detected_columns[:2]
                plt.scatter(self.df[x], self.df[y])
                plt.xlabel(x)
                plt.ylabel(y)

            elif plot_type == "pie":
                col = detected_columns[0]
                self.df[col].value_counts().plot(kind="pie", autopct="%1.1f%%")

            elif plot_type == "bar":
                col = detected_columns[0]
                self.df[col].value_counts().plot(kind="bar")

            else:
                col = detected_columns[0]
                if not pd.api.types.is_numeric_dtype(self.df[col]):
                    return "Histogram requires numeric column.", None
                self.df[col].dropna().hist()

        except Exception:
            plt.close(fig)
            return "Failed to generate chart.", None

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

        return "Here is the requested visualization.", image_base64