chat_prompt = """**Task:**  
### **Optimized Prompt for ChatGPT**  

You will receive **extracted data from a document**, and your task is to **convert it into a valid Salesforce-compatible XML format**.  

### **Key Rules:**  
- **Use only the provided data.** Do **not** create, modify, infer, or remove any data.  
- **Ensure the correct XML structure** by selecting an appropriate **root/header element** based on the nature of the data for Salesforce compatibility.  
- **Handle extracted text carefully**, considering spatial information (Axis data) to reconstruct meaningful content.  

### **Understanding Axis Data:**  
Each extracted line and extracted checkboxes includes positional coordinates:  

- **x** → Distance from the left side of the document.  
- **y** → Distance from the top of the document.  

#### **Example:**  
Hello  [Axis(x,y): (0.1,0.1)]  
World  [Axis(x,y): (0.3,0.1)]  
This   [Axis(x,y): (0.1,0.2)]  
Is     [Axis(x,y): (0.2,0.2)]  
ChatGPT[Axis(x,y): (0.3,0.2)]  

#### **Reconstructed Output (Logical Text Flow Based on Positioning):**
Hello World  
This Is ChatGPT 

#### **Extracted Key Value Pair Instructions:**
- Each key-value pair follows the format: Key: 'key' | Value: 'value'.
- Do not rephrase or modify the key or value in any way.
- Simply encapsulate the key-value pair within a wrapper container with an appropriate name.


#### **User's Data:**

The extracted data is provided below. Convert this into a Salesforce-compatible XML format while following the Response Guidelines.
### User's Data START:
{question}
### User's Data END


### **Response Guidelines:**
- Return only raw XML—no explanations, comments, or extra text.
- Ensure a well-formed, valid XML structure that adheres to Salesforce standards.
- Escape special characters (& → &amp;, < → &lt;, > → &gt;, etc.).
"""
