class ValidationService:

    @staticmethod
    def validate_dataset(df):

        missing_values = int(
            df.isnull().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        empty_columns = []

        for column in df.columns:

            if df[column].isnull().all():

                empty_columns.append(
                    column
                )

        quality_score = 100

        quality_score -= min(
            missing_values * 2,
            40
        )

        quality_score -= min(
            duplicate_rows * 5,
            30
        )

        quality_score -= min(
            len(empty_columns) * 10,
            30
        )

        quality_score = max(
            0,
            quality_score
        )

        warnings = []

        if missing_values > 0:

            warnings.append(
                f"{missing_values} missing values detected."
            )

        if duplicate_rows > 0:

            warnings.append(
                f"{duplicate_rows} duplicate rows detected."
            )

        if empty_columns:

            warnings.append(
                f"Empty columns detected: {', '.join(empty_columns)}"
            )

        return {
            "quality_score": quality_score,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "empty_columns": empty_columns,
            "warnings": warnings
        }