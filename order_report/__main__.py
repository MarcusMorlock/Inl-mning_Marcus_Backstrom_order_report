""""""

import logging

from . import (
    configure_log,
    LOGGER_NAME,
    ReportConfig,
    load_csv_to_dataframe,
    save_from_dataframe_to_csv,
    overview_order_report_dataframe,
    sales_by_category,
    returns_by_category,
    overview
)


def main() ->None:
    """Run Packet"""

    path_config = ReportConfig()
    path_config.ensure_directories()


    #Configure logging for application
    configure_log(log_path=path_config.log_path)

    logger = logging.getLogger(LOGGER_NAME)
    logger.info("Report from main started.")

    #Load Csv into DataFrame
    df = load_csv_to_dataframe(file_path=path_config.input_path)
    logger.info("Loaded from Main.")

    #Processes DataFrame and adding columns
    processed_df = overview_order_report_dataframe(df)
    logger.info("Processed from Main.")

    #Transform Processed DataFrame by selected params. 
    sales_by_region_df = sales_by_category(processed_df, "region")
    sales_by_product_category_df = sales_by_category(processed_df, "product_category")
    returns_by_category_df = returns_by_category(processed_df, "product_category")
    logger.info("Transformed from Main.")

    #Transform Overview.
    overview_df = overview(processed_df)
    logger.info("processes from Main.")

    #Save Four Dataframe´s into CSV into map data_output
    save_from_dataframe_to_csv(df=sales_by_region_df, file_path=f"{path_config.output_dir}/sales_by_region.csv")
    save_from_dataframe_to_csv(df=sales_by_product_category_df, file_path=f"{path_config.output_dir}/sales_by_category.csv")
    save_from_dataframe_to_csv(df=returns_by_category_df, file_path=f"{path_config.output_dir}/returns_by_category.csv")
    save_from_dataframe_to_csv(df=overview_df, file_path=f"{path_config.output_dir}/overview.csv")
    logger.info("Saved DataFrame to data_output from Main.")


if __name__ == "__main__":
    main()
