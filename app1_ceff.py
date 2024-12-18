# 檔案上傳

st.title("超市工具")

uploaded_file = st.file_uploader("請上傳包含 sales_volume, revenue, cost_of_goods_sold, store_location, date, product_id 的資料", type=["csv", "xlsx"])



if uploaded_file:

    # 讀取資料

    if uploaded_file.name.endswith(".csv"):

        data = pd.read_csv(uploaded_file)

    else:

        data = pd.read_excel(uploaded_file)



    st.write("資料預覽", data.head())



    # 選擇期間

    periods = data['period'].unique()

    previous_period = st.sidebar.selectbox("選擇上一期間", periods)

    current_period = st.sidebar.selectbox("選擇當前期間", periods)



    # Sidebar 篩選條件

    st.sidebar.header("篩選條件")

    store_location_filter = st.sidebar.selectbox("選擇店鋪位置", data['store_location'].unique())

    date_filter = st.sidebar.date_input("選擇日期", pd.to_datetime("2024-12-01"))

    product_filter = st.sidebar.multiselect("選擇產品", data['product_id'].unique(), default=data['product_id'].unique())



    # 篩選資料

    previous_data = data[

        (data['period'] == previous_period) &

        (data['store_location'] == store_location_filter) &

        (pd.to_datetime(data['date']) == pd.to_datetime(date_filter)) &

        (data['product_id'].isin(product_filter))

    ]



    current_data = data[

        (data['period'] == current_period) &

        (data['store_location'] == store_location_filter) &

        (pd.to_datetime(data['date']) == pd.to_datetime(date_filter)) &

        (data['product_id'].isin(product_filter))

    ]



    # 設定資料順序

    all_products = sorted(data['product_id'].unique())

    product_order = st.sidebar.multiselect("選擇畫圖順序", all_products, default=all_products)



    # 根據指定順序排序資料

    previous_data = previous_data.set_index('product_id').loc[product_order].reset_index()

    current_data = current_data.set_index('product_id').loc[product_order].reset_index()



    # 計算差異

    merged_data = previous_data.merge(current_data, on=['store_location', 'date', 'product_id'], suffixes=('_previous', '_current'))

    merged_data['sales_volume_diff'] = merged_data['sales_volume_current'] - merged_data['sales_volume_previous']

    merged_data['revenue_diff'] = merged_data['revenue_current'] - merged_data['revenue_previous']

    merged_data['cost_of_goods_sold_diff'] = merged_data['cost_of_goods_sold_current'] - merged_data['cost_of_goods_sold_previous']

    merged_data['sales_volume_ratio'] = merged_data['sales_volume_current'] / merged_data['sales_volume_previous']

    merged_data['revenue_ratio'] = merged_data['revenue_current'] / merged_data['revenue_previous']



    # 顯示差異表格

    st.subheader("期間差異表格")

    st.write(merged_data)



    # 繪製圖表

    st.subheader("圖表")

    # 圖表 1: 銷售量 vs 收入

    fig1, ax1 = plt.subplots()

    ax1.plot(merged_data['sales_volume_previous'], merged_data['revenue_previous'], label=f"{previous_period}: 銷售量 vs 收入", marker='o', linestyle='-')

    ax1.plot(merged_data['sales_volume_current'], merged_data['revenue_current'], label=f"{current_period}: 銷售量 vs 收入", marker='o', linestyle='-')

    ax1.set_xlabel("銷售量")

    ax1.set_ylabel("收入")

    ax1.legend()

    st.pyplot(fig1)


