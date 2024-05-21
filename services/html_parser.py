from bs4 import BeautifulSoup

def parse_html_to_text(html_file_path):
    # Charger le contenu HTML à partir du fichier
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Utiliser BeautifulSoup pour parser le contenu HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Trouver le titre de la conversation
    title_element = soup.find('title')
    current_topic = title_element.text.strip() if title_element else "pas trouvé"

    # Trouver tous les éléments de message et les noms d'utilisateurs
    message_elements = soup.find_all('div', class_='fui-ChatMessage__body')
    usernames = [element.text.strip() for element in soup.find_all('div', class_='fui-ChatMessage__author')]

    # Initialiser la liste des conversations
    concat_conversations = []

    # Initialiser les variables pour stocker les messages de la conversation en cours
    current_comments = []

    # Parcourir chaque élément de message
    for message_element, username in zip(message_elements, usernames):
        # Trouver le contenu du message
        message_content = message_element.find('div', class_='fui-Primitive')
        if message_content:
            message_text = message_content.text.strip()
            
            # Vérifier s'il y a un saut de ligne ou une date et une heure dans le commentaire
            if '\n' not in message_text and not any(char.isdigit() for char in message_text):
                # Ajouter le message à la liste des commentaires de la conversation en cours
                current_comments.append(message_text)

    # Ajouter la conversation à la liste de conversations
    concat_conversations.append({"topic": current_topic, "comments": current_comments})

    # Formater la sortie comme demandé avec retour à la ligne après chaque virgule
    formatted_comments = ['"' + comment.replace('"', '\\"').replace('\n', '\\n') + '"' for comment in current_comments]
    formatted_comments_with_line_breaks = [f"        {comment},\n" for comment in formatted_comments]
    formatted_conversation = (
        f"{{\n    \"topic\": \"{current_topic}\",\n    \"comments\": [\n{formatted_comments_with_line_breaks[0]}{'' if not formatted_comments_with_line_breaks[1:] else ''.join(formatted_comments_with_line_breaks[1:])[:-2]}\n    ]\n}}"
    )

    # Retourner la conversation formatée
    return formatted_conversation
