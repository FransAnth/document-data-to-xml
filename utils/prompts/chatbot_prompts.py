chat_prompt = """**Task:**  
### **Optimized Prompt for ChatGPT**  

You will receive **extracted data from a document**, and your task is to **convert it into a valid Salesforce-compatible XML format**.  

### **Key Rules:**  
- **Use only the provided data.** Do **not** create, modify, infer, or remove any data.  
- **Ensure the correct XML structure** by selecting an appropriate **root/header element** based on the nature of the data for Salesforce compatibility.  
- **Handle extracted text carefully**, considering spatial information (Axis data) to reconstruct meaningful content.  
- **Table data will be provided separately**—do not retain table-like structures from the initial extracted text.  

### **Understanding Axis Data:**  
Each extracted line and extracted checkboxes includes positional coordinates:  

- **x** → Distance from the left side of the document.  
- **y** → Distance from the top of the document.  

#### **Example Input:**  
Hello  [Axis(x,y): (0.1,0.1)]  
World  [Axis(x,y): (0.3,0.1)]  
This   [Axis(x,y): (0.1,0.2)]  
Is     [Axis(x,y): (0.2,0.2)]  
ChatGPT[Axis(x,y): (0.3,0.2)]  

#### **Reconstructed Output (Logical Text Flow Based on Positioning):**
Hello World  
This Is ChatGPT 

#### **Extracted Checkboxes Instructions:**
- Each checkbox includes positional coordinates.
- Use these coordinates to determine which extracted line of text the checkbox is closest to. 
- The closest extracted line to a checkbox represents the information related to that checkbox's status.
- Assign the checkbox status to its corresponding line to ensure the line has the necessary status information.

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
