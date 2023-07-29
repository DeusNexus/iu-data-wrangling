'''
The file contains model of each data/logs file's columns and dtypes. Used for generating DataFrames from CSV file data and setting the correct types and datetime columns.
CSV are unable to store these formats natively, when the Pandas DataFrame is saved to HDF5 file the metadata about the data types is carried over.
'''

model = {
    "api_data": {
        "parse_dates":["timestamp"],
        "index":"timestamp",
        "cols": {
            "timestamp":"str",
            "open":"float",
            "high":"float",
            "low":"float",
            "close":"float"
        }
    },

    "api_logs": {
        "parse_dates":["start_dt","response_dt"],
        "index":"start_dt",
        "cols": {
            "start_dt":"str",
            "response_dt":"str",
            "error":"str",
            "status_code":"int64",
            "success":"bool"
        }
    },

    "html_data": {
        "parse_dates":["updated","time_utc","time_utc_at_epicenter"],
        "index":"updated",
        "cols": {
            "id":"str",
            "title":"str",
            "updated":"str",
            "link_href":"str",
            "num_of_reports":"float",
            "time_utc":"str",
            "time_utc_at_epicenter":"str",
            "location_coordinates":"str",
            "depth_string":"str",
            "depth_km":"float",
            "depth_mi":"float",
            "georss_point":"str",
            "georss_elev":"str",
            "cat_age":"str",
            "cat_mag":"str",
            "cat_mag_shaking":"str",
            "cat_mag_damage":"str",
            "cat_contributor":"str",
            "cat_author":"str"
        }
    },

    "html_logs": {
        "parse_dates":["timestamp"],
        "index":"timestamp",
        "cols": {
            "timestamp":"str",
            "url":"str",
            "err_msg":"str",
            "err_obj":"str",
            "data":"str",
            "req_status":"str",
            "method":"str",
            "execution_time_ms":"float"
        }
    },

    "wss_data": {
        "parse_dates":["timestamp"],
        "index":"timestamp",
        "cols": {
            "timestamp":"str",
            "symbol":"str",
            "side":"str",
            "size":"int64",
            "price":"float",
            "tickDirection":"str",
            "trdMatchID":"str",
            "grossValue":"float64",
            "homeNotional":"float64",
            "foreignNotional":"float64",
            "trdType":"str"
        }
    },


    "wss_logs": {   
        "parse_dates":["timestamp","last_update"],
        "index":"timestamp",
        "cols": {
            "timestamp":"str",
            "last_update":"str",
            "init":"bool",
            "num_updates":"int64",
            "num_errors":"int64",
            "total_pong":"int64",
            "total_timeout":"int64",
            "total_reconnect":"int64",
            "func_name":"str",
            "state":"str",
            "update":"str",
            "message":"str"
        }
    }
}