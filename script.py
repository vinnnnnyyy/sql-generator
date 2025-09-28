# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import json
import os
from google import genai
from google.genai import types


class SQLQueryGenerator:
    def __init__(self):
        self.client = genai.Client(
            api_key="AIzaSyANefEtYeJWt4jNQEMSyFTAVFh_eNL9r2s"
        )
        self.history_file = "query_history.json"
        self.query_history = self.load_history()
        
    def load_history(self):
        """Load query history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Save query history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.query_history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save history: {e}")
    
    def add_to_history(self, question, sql_query):
        """Add a query to history (keep last 10 queries)"""
        self.query_history.append({
            "question": question,
            "sql_query": sql_query
        })
        # Keep only last 10 queries
        if len(self.query_history) > 10:
            self.query_history = self.query_history[-10:]
        self.save_history()
    
    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("SQL Query Generator")
        print("="*50)
        print("1. Generate new SQL query")
        print("2. View last query")
        print("3. View query history")
        print("4. Use a previous query")
        print("5. Clear history")
        print("6. Exit")
        print("-"*50)
        
    def generate_query(self, question):
        """Generate SQL query from question"""
        model = "gemini-2.5-pro"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=f"""You are a SQL query generator. Generate ONLY the SQL query without any explanation or additional text.

Question: {question}

Please provide only the SQL query as output, nothing else."""),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(
                thinking_budget=-1,
            ),
        )

        response_text = ""
        print("\nGenerating SQL query...")
        for chunk in self.client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                response_text += chunk.text
        
        # Extract only the SQL query (remove any markdown formatting or extra text)
        lines = response_text.strip().split('\n')
        sql_query = ""
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('```') and not line.lower().startswith('here') and not line.lower().startswith('the query'):
                sql_query += line + "\n"
        
        return sql_query.strip()
    
    def handle_new_query(self):
        """Handle new query generation"""
        question = input("\nEnter your SQL question: ").strip()
        if not question:
            print("No question entered.")
            return
            
        sql_query = self.generate_query(question)
        print("\n" + "-"*50)
        print("Generated SQL Query:")
        print("-"*50)
        print(sql_query)
        print("-"*50)
        
        # Save to history
        self.add_to_history(question, sql_query)
        print("\n✓ Query saved to history")
    
    def show_last_query(self):
        """Show the last query from history"""
        if not self.query_history:
            print("\nNo query history available.")
            return
            
        last = self.query_history[-1]
        print("\n" + "-"*50)
        print("Last Query:")
        print("-"*50)
        print(f"Question: {last['question']}")
        print(f"\nSQL Query:\n{last['sql_query']}")
        print("-"*50)
    
    def show_history(self):
        """Show all query history"""
        if not self.query_history:
            print("\nNo query history available.")
            return
            
        print("\n" + "="*50)
        print("Query History (Most Recent First):")
        print("="*50)
        
        for i, item in enumerate(reversed(self.query_history), 1):
            print(f"\n{i}. Question: {item['question'][:50]}{'...' if len(item['question']) > 50 else ''}")
            print(f"   SQL: {item['sql_query'][:100]}{'...' if len(item['sql_query']) > 100 else ''}")
            print("-"*50)
    
    def use_previous_query(self):
        """Allow user to select and regenerate a previous query"""
        if not self.query_history:
            print("\nNo query history available.")
            return
            
        print("\n" + "="*50)
        print("Select a Previous Query:")
        print("="*50)
        
        for i, item in enumerate(reversed(self.query_history), 1):
            print(f"{i}. {item['question'][:70]}{'...' if len(item['question']) > 70 else ''}")
        
        print("0. Cancel")
        print("-"*50)
        
        try:
            choice = int(input("\nEnter number (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(self.query_history):
                item = self.query_history[-choice]
                print(f"\nUsing question: {item['question']}")
                
                # Ask if user wants to regenerate or just view
                regen = input("Regenerate query? (y/n): ").lower()
                if regen == 'y':
                    sql_query = self.generate_query(item['question'])
                    print("\n" + "-"*50)
                    print("Regenerated SQL Query:")
                    print("-"*50)
                    print(sql_query)
                    print("-"*50)
                    self.add_to_history(item['question'], sql_query)
                else:
                    print("\n" + "-"*50)
                    print("Stored SQL Query:")
                    print("-"*50)
                    print(item['sql_query'])
                    print("-"*50)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def clear_history(self):
        """Clear all query history"""
        confirm = input("\nAre you sure you want to clear all history? (y/n): ").lower()
        if confirm == 'y':
            self.query_history = []
            self.save_history()
            if os.path.exists(self.history_file):
                try:
                    os.remove(self.history_file)
                except:
                    pass
            print("✓ History cleared successfully.")
        else:
            print("History clear cancelled.")
    
    def run(self):
        """Main program loop"""
        print("\nWelcome to SQL Query Generator!")
        print("This tool remembers your queries and provides a menu system.")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\nEnter your choice (1-6): ").strip()
                
                if choice == '1':
                    self.handle_new_query()
                elif choice == '2':
                    self.show_last_query()
                elif choice == '3':
                    self.show_history()
                elif choice == '4':
                    self.use_previous_query()
                elif choice == '5':
                    self.clear_history()
                elif choice == '6':
                    print("\nThank you for using SQL Query Generator!")
                    print("Your query history has been saved.")
                    print("Goodbye!")
                    break
                else:
                    print("\nInvalid choice. Please select 1-6.")
                    
                # Pause before showing menu again (except for exit)
                if choice != '6':
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user.")
                save = input("Save history before exit? (y/n): ").lower()
                if save == 'y':
                    self.save_history()
                    print("✓ History saved.")
                print("Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try again.")


if __name__ == "__main__":
    generator = SQLQueryGenerator()
    generator.run()