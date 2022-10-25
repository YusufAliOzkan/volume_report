import pandas as pd
import openpyxl
# from urlextract import URLExtract
import re
import numpy as np
from operator import index
import io
import streamlit as st
from io import BytesIO
from datetime import date

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import pandas as pd
from io import StringIO

# Setting the app page layout
st.set_page_config(layout = "centered", page_title='Spiral Symplectic Report processor')
st.markdown("# Spiral Symplectic Report processor")

# st.sidebar.markdown("# Spiral Symplectic Report processor")
st.markdown('* Copy the text of volume report') 
st.markdown('* Paste into the box below')
st.markdown("* Press **Ctrl + Enter** to apply")
st.markdown("* Press 'Download report'")            

txt = st.text_area('Paste the volume report here:', '''
    ''')
df = pd.DataFrame(StringIO(txt))

if df is not None:
    df1 = df.drop([0])
    df1[1] = df1[0].str.extract('Spiral:(.*)')
    pattern = r'(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}[-a-zA-Z0-9()@:%_+.~#?&/=]*)' 
    df1[2] = df1[1].str.extract(pattern, expand=True)
    df_url = df1.drop([0,1], axis=1)

    def make_hyperlink(value):
        url = "{}"
        return '=HYPERLINK("%s", "%s")' % (url.format(value), value)
    df_url[2] = df_url[2].apply(lambda x: make_hyperlink(x))
    df_split = np.array_split(df_url, 2)
    if df_split is not None:
        buffer = io.BytesIO()
        today = date.today().isoformat()
        a = 'Weekly Spiral Symplectic Report - '+today
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write each dataframe to a different worksheet.
            df_split[0].to_excel(writer, sheet_name='K', header=False, index=False)
            df_split[1].to_excel(writer, sheet_name='Y', header=False, index=False)

            # Close the Pandas Excel writer and output the Excel file to the buffer
            writer.save()

        st.download_button(
            label="Download report",
            data=buffer,
            file_name= a+".xlsx",
            mime="application/vnd.ms-excel"
        )