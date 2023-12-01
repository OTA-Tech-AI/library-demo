import pandas as pd

df_qa = pd.read_csv("qa.csv", index_col=0, encoding='ISO-8859-1')
df_knowledge = pd.read_csv("knowledge.csv", index_col=0, encoding='ISO-8859-1')
filtered_df_qa = df_qa[df_qa['status'] == 0]
filtered_df_knowledge = df_knowledge[df_knowledge['status'] == 0]

# Ensure all data is in string format
filtered_df_qa = filtered_df_qa.astype(str)
filtered_df_knowledge = filtered_df_knowledge.astype(str)

# Format the strings with labels and new lines
combined_qa = filtered_df_qa.apply(lambda x: f"Question: {x['question']}\nAnswer: {x['answer']}\n", axis=1)
combined_knowledge = filtered_df_knowledge.apply(lambda x: f"Title: {x['title']}\nKnowledge: {x['knowledge']}\n", axis=1)

# Convert to string
combined_qa_str = '\n'.join(combined_qa)
combined_knowledge_str = '\n'.join(combined_knowledge)

# Concatenate the two strings with a newline in between
final_combined_string = combined_qa_str + '\n' + combined_knowledge_str

print(final_combined_string)
