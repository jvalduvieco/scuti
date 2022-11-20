def print_traceback(logger, tb):
    local_vars = {}
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        line_no = tb.tb_lineno
        # Prepend desired color (e.g. RED) to line
        logger.error(f"\tFile {filename} line {line_no}, in {name}")

        local_vars = tb.tb_frame.f_locals
        tb = tb.tb_next
    logger.error(f"Local variables in top frame: \n\t{local_vars}")
