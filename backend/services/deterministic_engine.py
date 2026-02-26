def handle(self, question: str):

    q = question.lower().strip()
    tokens = q.replace(",", "").split()

    filters = {}

    # ====================================================
    # 1️⃣ FILTER DETECTION
    # ====================================================

    if "male" in tokens:
        filters["Sex"] = "male"

    if "female" in tokens:
        filters["Sex"] = "female"

    if "first" in tokens or "1st" in tokens:
        filters["Pclass"] = 1

    if "second" in tokens or "2nd" in tokens:
        filters["Pclass"] = 2

    if "third" in tokens or "3rd" in tokens:
        filters["Pclass"] = 3

    if "survived" in tokens:
        filters["Survived"] = 1

    if "died" in tokens or "dead" in tokens:
        filters["Survived"] = 0

    df_filtered = self.df.copy()

    for col, val in filters.items():
        df_filtered = df_filtered[df_filtered[col] == val]

    # ====================================================
    # 2️⃣ GROUPED COUNTS (MUST BE ABOVE TOTAL COUNT)
    # ====================================================

    # Embarked grouped count
    if "embarked" in q and ("how many" in q or "number" in q):
        counts = self.df["Embarked"].value_counts()
        result = "\n".join(
            f"{k}: {v}" for k, v in counts.items()
        )
        return f"Passengers embarked from each port:\n{result}"

    # Generic group by
    if "how many" in q and "by" in q:
        for col in self.df.columns:
            if col.lower() in q:
                counts = self.df[col].value_counts()
                result = "\n".join(
                    f"{k}: {v}" for k, v in counts.items()
                )
                return f"Passenger count by {col}:\n{result}"

    # ====================================================
    # 3️⃣ SIMPLE TOTAL COUNT (MOVE BELOW GROUPED)
    # ====================================================

    if "how many passengers" in q and not filters:
        return f"There were {len(self.df)} passengers in total."

    # ====================================================
    # 4️⃣ FILTERED COUNT
    # ====================================================

    if ("how many" in q or "number" in q) and filters:
        count = len(df_filtered)
        return f"There were {count} passengers matching the criteria."

    # ====================================================
    # 5️⃣ PERCENTAGE
    # ====================================================

    if "percentage" in q and filters:
        total = len(self.df)
        count = len(df_filtered)
        pct = (count / total) * 100
        return f"{pct:.2f}% of passengers match the given criteria."

    # Special male/female percentage
    if "percentage" in q and ("male" in q or "female" in q):
        total = len(self.df)
        gender = "male" if "male" in q else "female"
        count = len(self.df[self.df["Sex"] == gender])
        pct = (count / total) * 100
        return f"{pct:.2f}% of passengers were {gender}."

    # ====================================================
    # 6️⃣ NUMERIC OPERATIONS
    # ====================================================

    numeric_columns = self.df.select_dtypes(include="number").columns

    if "average" in q or "mean" in q:
        for col in numeric_columns:
            if col.lower() in q:
                avg = df_filtered[col].mean()
                return f"The average {col} was {avg:.2f}."

    if "maximum" in q or "max" in q:
        for col in numeric_columns:
            if col.lower() in q:
                val = df_filtered[col].max()
                return f"The maximum {col} was {val}."

    if "minimum" in q or "min" in q:
        for col in numeric_columns:
            if col.lower() in q:
                val = df_filtered[col].min()
                return f"The minimum {col} was {val}."

    # ====================================================
    # 7️⃣ SURVIVAL RATE
    # ====================================================

    if "survival rate" in q and "by" in q:
        for col in self.df.columns:
            if col.lower() in q:
                rates = (
                    self.df.groupby(col)["Survived"]
                    .mean() * 100
                )
                result = "\n".join(
                    f"{k}: {v:.2f}%"
                    for k, v in rates.items()
                )
                return f"Survival rate by {col}:\n{result}"

    if "highest" in q and "survival rate" in q:
        rates = (
            self.df.groupby("Pclass")["Survived"]
            .mean()
            .sort_values(ascending=False)
        )
        top_class = rates.index[0]
        top_rate = rates.iloc[0] * 100
        return f"Class {top_class} had the highest survival rate at {top_rate:.2f}%."

    if "lowest" in q and "survival rate" in q:
        rates = (
            self.df.groupby("Pclass")["Survived"]
            .mean()
            .sort_values()
        )
        bottom_class = rates.index[0]
        bottom_rate = rates.iloc[0] * 100
        return f"Class {bottom_class} had the lowest survival rate at {bottom_rate:.2f}%."

    # ====================================================
    # 8️⃣ AGE SPECIAL
    # ====================================================

    if "oldest" in q:
        return f"The oldest passenger was {df_filtered['Age'].max()} years old."

    if "youngest" in q:
        return f"The youngest passenger was {df_filtered['Age'].min()} years old."

    return None