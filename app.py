
import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(
    page_title="Knapsack Optimizer",
    page_icon="🎒",
    layout="wide"
)

st.title("🎒 0/1 Knapsack Problem")
st.write(
    "Select the best combination of items without "
    "exceeding the maximum knapsack capacity."
)

# 2. Default items
default_items = pd.DataFrame({
    "Item": ["Laptop", "Book", "Camera", "Phone"],
    "Weight": [3, 2, 4, 1],
    "Value": [40, 25, 50, 15]
})

# 3. User inputs
capacity = st.number_input(
    "Knapsack Capacity",
    min_value=1,
    max_value=10000,
    value=7,
    step=1
)

st.subheader("Available Items")

items_df = st.data_editor(
    default_items,
    num_rows="dynamic",
    use_container_width=True,
    key="items_editor",
    column_config={
        "Item": st.column_config.TextColumn(
            "Item Name",
            required=True
        ),
        "Weight": st.column_config.NumberColumn(
            "Weight",
            min_value=1,
            step=1,
            required=True
        ),
        "Value": st.column_config.NumberColumn(
            "Value",
            min_value=0,
            step=1,
            required=True
        )
    }
)

# 4. Knapsack algorithm using Dynamic Programming
def knapsack(items, capacity):
    n = len(items)

    # dp[i][w] = maximum value using the first i items
    # with a capacity of w
    dp = [
        [0] * (capacity + 1)
        for _ in range(n + 1)
    ]

    for i in range(1, n + 1):
        weight = items[i - 1]["weight"]
        value = items[i - 1]["value"]

        for w in range(capacity + 1):

            # Option 1: Exclude the current item
            dp[i][w] = dp[i - 1][w]

            # Option 2: Include the current item
            if weight <= w:
                candidate = (
                    value + dp[i - 1][w - weight]
                )

                dp[i][w] = max(
                    dp[i][w],
                    candidate
                )

    # 5. Backtrack to identify selected items
    selected_items = []
    remaining_capacity = capacity

    for i in range(n, 0, -1):
        if (
            dp[i][remaining_capacity]
            != dp[i - 1][remaining_capacity]
        ):
            item = items[i - 1]
            selected_items.append(item)
            remaining_capacity -= item["weight"]

    selected_items.reverse()

    return dp[n][capacity], selected_items, dp


# 6. Run the algorithm
if st.button("🚀 Run Knapsack Algorithm", type="primary"):

    # Validate input data
    if items_df.empty:
        st.error("Please add at least one item.")
        st.stop()

    if items_df.isnull().any().any():
        st.error("Please complete all item fields.")
        st.stop()

    if items_df["Item"].astype(str).str.strip().eq("").any():
        st.error("Every item must have a name.")
        st.stop()

    if (
        (items_df["Weight"] <= 0).any()
        or (items_df["Value"] < 0).any()
    ):
        st.error(
            "Weight must be positive and value must be non-negative."
        )
        st.stop()

    if (
        (items_df["Weight"] % 1 != 0).any()
        or (items_df["Value"] % 1 != 0).any()
    ):
        st.error("Please use integer weights and values.")
        st.stop()

    # Convert the DataFrame into a list of dictionaries
    items = [
        {
            "name": str(row["Item"]),
            "weight": int(row["Weight"]),
            "value": int(row["Value"])
        }
        for _, row in items_df.iterrows()
    ]

    # Execute the algorithm
    max_value, selected_items, dp = knapsack(
        items,
        int(capacity)
    )

    total_weight = sum(
        item["weight"] for item in selected_items
    )

    # 7. Display results
    st.divider()
    st.subheader("📊 Optimization Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Maximum Value", max_value)
    col2.metric(
        "Total Weight",
        f"{total_weight} / {int(capacity)}"
    )
    col3.metric(
        "Selected Items",
        len(selected_items)
    )

    if selected_items:
        st.success("Optimal item combination found!")

        result_df = pd.DataFrame([
            {
                "Item": item["name"],
                "Weight": item["weight"],
                "Value": item["value"]
            }
            for item in selected_items
        ])

        st.dataframe(
            result_df,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("The optimal solution is to select no items.")

    # 8. Display the Dynamic Programming table
    with st.expander("View Dynamic Programming Table"):
        st.write(
            "Each cell dp[i][w] represents the maximum value "
            "obtainable using the first i items with capacity w."
        )

        dp_df = pd.DataFrame(
            dp,
            index=[f"Items {i}" for i in range(len(dp))],
            columns=[
                f"Capacity {w}"
                for w in range(int(capacity) + 1)
            ]
        )

        st.dataframe(
            dp_df,
            use_container_width=True
        )
