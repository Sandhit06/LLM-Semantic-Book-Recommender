import pandas as pd
import numpy as np
import gradio as gr

# Load book data
books = pd.read_csv("books_with_emotions.csv")
books["large_thumbnail"] = books["thumbnail"] + "&fife=w800"
books["large_thumbnail"] = np.where(
    books["large_thumbnail"].isna(),
    "cover-not-found.jpg",
    books["large_thumbnail"],
)

def recommend_books(query: str, category: str, tone: str):
    # Select books randomly instead of using embeddings
    book_recs = books.copy()

    if category != "All":
        book_recs = book_recs[book_recs["simple_categories"] == category]

    if tone == "Happy":
        book_recs = book_recs.sort_values(by="joy", ascending=False)
    elif tone == "Surprising":
        book_recs = book_recs.sort_values(by="surprise", ascending=False)
    elif tone == "Angry":
        book_recs = book_recs.sort_values(by="anger", ascending=False)
    elif tone == "Suspenseful":
        book_recs = book_recs.sort_values(by="fear", ascending=False)
    elif tone == "Sad":
        book_recs = book_recs.sort_values(by="sadness", ascending=False)

    recommendations = book_recs.sample(n=16)  # Randomly pick 16 books

    results = []
    for _, row in recommendations.iterrows():
        description = row["description"]
        truncated_description = " ".join(description.split()[:30]) + "..."

        authors_split = row["authors"].split(";")
        if len(authors_split) == 2:
            authors_str = f"{authors_split[0]} and {authors_split[1]}"
        elif len(authors_split) > 2:
            authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
        else:
            authors_str = row["authors"]

        caption = f"{row['title']} by {authors_str}: {truncated_description}"
        results.append((row["large_thumbnail"], caption))

    return results

# UI setup
categories = ["All"] + sorted(books["simple_categories"].unique())
tones = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]

with gr.Blocks(theme=gr.themes.Glass()) as dashboard:
    gr.Markdown("# Semantic Book Recommender")

    with gr.Row():
        user_query = gr.Textbox(label="Please enter a description of a book:", placeholder="e.g., A story about forgiveness")
        category_dropdown = gr.Dropdown(choices=categories, label="Select a category:", value="All")
        tone_dropdown = gr.Dropdown(choices=tones, label="Select an emotional tone:", value="All")
        submit_button = gr.Button("Find recommendations")

    gr.Markdown("## Recommendations")
    output = gr.Gallery(label="Recommended books", columns=8, rows=2)

    submit_button.click(fn=recommend_books, inputs=[user_query, category_dropdown, tone_dropdown], outputs=output)

if __name__ == "__main__":
    dashboard.launch()








# Incase the Gemini AI quota gets exhausted try running this to see the Gradio UI
# import pandas as pd
# import numpy as np
# import gradio as gr
#
# # Load book data
# books = pd.read_csv("books_with_emotions.csv")
# books["large_thumbnail"] = books["thumbnail"] + "&fife=w800"
# books["large_thumbnail"] = np.where(
#     books["large_thumbnail"].isna(),
#     "cover-not-found.jpg",
#     books["large_thumbnail"],
# )
#
# def recommend_books(query: str, category: str, tone: str):
#     # Select books randomly instead of using embeddings
#     book_recs = books.copy()
#
#     if category != "All":
#         book_recs = book_recs[book_recs["simple_categories"] == category]
#
#     if tone == "Happy":
#         book_recs = book_recs.sort_values(by="joy", ascending=False)
#     elif tone == "Surprising":
#         book_recs = book_recs.sort_values(by="surprise", ascending=False)
#     elif tone == "Angry":
#         book_recs = book_recs.sort_values(by="anger", ascending=False)
#     elif tone == "Suspenseful":
#         book_recs = book_recs.sort_values(by="fear", ascending=False)
#     elif tone == "Sad":
#         book_recs = book_recs.sort_values(by="sadness", ascending=False)
#
#     recommendations = book_recs.sample(n=16)  # Randomly pick 16 books
#
#     results = []
#     for _, row in recommendations.iterrows():
#         description = row["description"]
#         truncated_description = " ".join(description.split()[:30]) + "..."
#
#         authors_split = row["authors"].split(";")
#         if len(authors_split) == 2:
#             authors_str = f"{authors_split[0]} and {authors_split[1]}"
#         elif len(authors_split) > 2:
#             authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
#         else:
#             authors_str = row["authors"]
#
#         caption = f"{row['title']} by {authors_str}: {truncated_description}"
#         results.append((row["large_thumbnail"], caption))
#
#     return results
#
# # UI setup
# categories = ["All"] + sorted(books["simple_categories"].unique())
# tones = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]
#
# with gr.Blocks(theme=gr.themes.Glass()) as dashboard:
#     gr.Markdown("# Semantic Book Recommender")
#
#     with gr.Row():
#         user_query = gr.Textbox(label="Please enter a description of a book:", placeholder="e.g., A story about forgiveness")
#         category_dropdown = gr.Dropdown(choices=categories, label="Select a category:", value="All")
#         tone_dropdown = gr.Dropdown(choices=tones, label="Select an emotional tone:", value="All")
#         submit_button = gr.Button("Find recommendations")
#
#     gr.Markdown("## Recommendations")
#     output = gr.Gallery(label="Recommended books", columns=8, rows=2)
#
#     submit_button.click(fn=recommend_books, inputs=[user_query, category_dropdown, tone_dropdown], outputs=output)
#
# if __name__ == "__main__":
#     dashboard.launch()
