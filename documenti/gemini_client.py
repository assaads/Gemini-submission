import os
import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

DOCUMENTATION_SNAPSHOT_DIR = './snapshots/documentation-snapshot/'

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 50
}

safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

chat = model.start_chat()

def init(codebase):
    define_format()
    send_codebase(codebase)

def define_format():
    print("Initializing gemini agent")
    prompt = """
    I would like you to act as a professional/expert developer and technical architect.
    I am about to send you the full codebase of a project. After I do, I will start giving you requests regarding the code, mainly aimed at creating documentation for the codebase.
    Every time I request something from you I would like you to give me the answer in the format below (even if I asked you about a documentation regarding the code that you don't find or deem not applicable in the specific source code I would still like you to give me your answer in the following format without anything else before or after in the chat): 
    ---
    title: Example Guide
    description: A guide in my new Starlight docs site.
    ---

    don't include anything before this:

    ---
    title: Example Guide
    description: A guide in my new Starlight docs site.
    ---
    
    as the page always starts with it. Also, don't add a heading1 title after this section again but start directly with the content after.

    Moreover, if requested to create a page in a different language, only what comes after "title:" and "description:" is in a different language for the start of the page.
    for example:
    for French:
    
    ---
    title: Bonjour 
    description: comment ca va
    ---
    

    use headings as shown below:
    # Heading1
    ## Heading2
    ### Heading3
    #### Heading4

    Guides lead a user through a specific task they want to accomplish, often with a sequence of steps.
    Writing a good guide requires thinking about what your users are trying to do. (this is a random text, text is used as normal)

    - bullet point is used as such as well
    Links are done this way: [name](link itself). for example: [about reference](https://diataxis.fr/reference/)

    Additional components I would like you to focus on include, but are not limited to, the following:

    **Tabs:**
    - Use <Tabs> and <TabItem> components to create a tabbed interface. For example:
    ```
    import { Tabs, TabItem } from '@astrojs/starlight/components';

    <Tabs>
      <TabItem label="Stars" icon="star">
        Sirius, Vega, Betelgeuse
      </TabItem>
      <TabItem label="Moons" icon="moon">
        Io, Europa, Ganymede
      </TabItem>
    </Tabs>
    ```
    - To synchronize related tabs, add an identical syncKey property to each <Tabs> component.

    **Cards:**
    - Use the <Card> component to display content in a box matching Starlight’s styles. For example:
    ```
    import { Card, CardGrid } from '@astrojs/starlight/components';

    <Card title="Check this out">Interesting content you want to highlight.</Card>
    <CardGrid>
      <Card title="Stars" icon="star">
        Sirius, Vega, Betelgeuse
      </Card>
      <Card title="Moons" icon="moon">
        Io, Europa, Ganymede
      </Card>
    </CardGrid>
    ```

    **Link Cards:**
    - Use the <LinkCard> component to link prominently to different pages. For example:
    ```
    import { LinkCard, CardGrid } from '@astrojs/starlight/components';

    <LinkCard
      title="Customizing Starlight"
      description="Learn how to make your Starlight site your own with custom styles, fonts, and more."
      href="/guides/customization/"
    />
    <CardGrid>
      <LinkCard title="Authoring Markdown" href="/guides/authoring-content/" />
      <LinkCard title="Components" href="/guides/components/" />
    </CardGrid>
    ```

    **Asides:**
    - Use the <Aside> component to display secondary information alongside the main content. For example:
    ```
    import { Aside } from '@astrojs/starlight/components';

    <Aside>A default aside without a custom title.</Aside>
    <Aside type="caution" title="Watch out!">A warning aside *with* a custom title.</Aside>
    ```

    **File Tree:**
    - Use the <FileTree> component to display the structure of a directory with file icons and collapsible sub-directories. For example:
    ```
    import { FileTree } from '@astrojs/starlight/components';

    <FileTree>
      - astro.config.mjs an **important** file
      - package.json
      - README.md
      - src
        - components
          - **Header.astro**
        - …
      - pages/
    </FileTree>
    ```

    **Steps:**
    - Use the <Steps> component to style numbered lists of tasks. This is useful for more complex step-by-step guides where each step needs to be clearly highlighted. For example:
    ```
    import { Steps } from '@astrojs/starlight/components';

    <Steps>
      1. Import the component into your MDX file:
         ```js
         import { Steps } from '@astrojs/starlight/components';
         ```
      2. Wrap `<Steps>` around your ordered list items.
    </Steps>
    ```

    **Badges:**
    - Use the <Badge> component to display small pieces of information, such as status or labels. For example:
    ```
    import { Badge } from '@astrojs/starlight/components';

    <Badge text="New" variant="tip" size="small" />
    <Badge text="Deprecated" variant="caution" size="medium" />
    <Badge text="Starlight" variant="note" size="large" />
    <Badge text="Custom" variant="success" style={{ fontStyle: 'italic' }} />
    ```

    Please incorporate these components into the documentation where appropriate to enhance the user experience. When generating or updating documentation, consider how these UI elements can improve clarity, interactivity, and visual appeal. 

    Make sure to give me the answer in the following format without anything else before or after in the chat:
    ---
    title: Example Guide
    description: A guide in my new Starlight docs site.
    ---

    """
    text_response = []
    responses = chat.send_message(prompt, stream=True,
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    for chunk in responses:
        text_response.append(chunk.text)
    print("Finished defining UI format to AI")
    return "".join(text_response)

def send_codebase(codebase: str):
    prompt = f"""
    Here is the entire codebase of the project. I have put the name of the folder and files about each of their content for clarity.
    Keep in mind that I will be asking you documentation generation request following it.
    Here is the entire codebase:
    {codebase}
    """
    text_response = []
    responses = chat.send_message(prompt, stream=True,
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    for chunk in responses:
        text_response.append(chunk.text)
    print("Finished sending the codebase to the AI")
    return "".join(text_response)

def request_documentation(documentation_subject: str, language: str, update=False):
    add_language = ""
    if language != "":
        add_language = f" in the {language} language"
    
    if update == True:
        prompt = f"""
        In the format requested previously (even if I asked you to generate a documentation that you don't find or deem not applicable in the specific source code I would still like you to give me your answer in the format requested previously, and don't add any text before or after that's not in the format in your answer) and based on the change in the codebase sent, please recreate a documentation document for the following section and its description{add_language}:
        {documentation_subject}
        """
    else:
        prompt = f"""
        In the format requested previously (even if I asked you to generate a documentation that you don't find or deem not applicable in the specific source code I would still like you to give me your answer in the format requested previously, and don't add any text before or after that's not in the format in your answer) and based on the codebase sent, please create a documentation document for the following section and its description{add_language}:
        {documentation_subject}
        """
    text_response = []
    responses = chat.send_message(prompt, stream=True,
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    for chunk in responses:
        text_response.append(chunk.text)
    # print(f"Finished generating documentation for {documentation_subject}")
    return "".join(text_response)

def send_existing_documentation(project_name):
    """Send the existing documentation to the AI for context."""
    # Define the path to the documentation snapshot file for the project
    snapshot_file = os.path.join(DOCUMENTATION_SNAPSHOT_DIR, project_name, f'{project_name}_doc_snapshot.json')
    
    combined_output = ""
    
    if os.path.exists(snapshot_file):
        # Load the snapshot file
        with open(snapshot_file, 'r', encoding='utf-8') as f:
            doc_snapshot = json.load(f)
        
        # Iterate over the keys (representing the section paths) and their content
        for key, content in doc_snapshot.items():
            # Append the directory structure and content to the combined output
            combined_output += f"# Directory: {os.path.dirname(key)}\n"
            combined_output += f"# File: {os.path.basename(key)}\n\n"
            combined_output += content + "\n\n"
    else:
        print(f"No documentation snapshot found for project: {project_name}")
        return ""

    # Send the combined output to the AI
    prompt = f"Here is the existing documentation for the project '{project_name}'. Please use this for context when updating the documentation based on changes:\n\n{combined_output}"
    
    text_response = []
    responses = chat.send_message(prompt, stream=True,
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    for chunk in responses:
        text_response.append(chunk.text)
    
    print("Finished sending the existing documentation to the AI")
    return "".join(text_response)


def send_updated_code(combined_changes: str):
    """
    Requests the AI to identify and generate updates for the necessary documentation sections.
    
    The AI's response will include the directory path of each documentation section followed by its updated content.
    
    Parameters:
    - combined_changes (str): The combined changes in the codebase.
    - language (str): The target language for the documentation.
    
    Returns:
    - str: The AI's response containing updated documentation sections.
    """
    print("Requesting updated documentation from AI")
    
    text_response = []
    responses = chat.send_message(combined_changes, stream=True,
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    for chunk in responses:
        text_response.append(chunk.text)
    
    return "".join(text_response)
