from database.db_connect import DBConnection


QUIZ_SEED = [
    ("Nigeria", "Which fabric is strongly associated with Yoruba celebrations?", "Aso oke", "Denim", "Tweed", "Flannel", "a", "Aso oke is a traditional Yoruba woven fabric used at ceremonies."),
    ("Nigeria", "What is jollof rice commonly served at in Nigeria?", "Only breakfast", "Parties and celebrations", "Religious fasting only", "School exams only", "b", "Jollof rice is a popular celebration food across Nigeria and West Africa."),
    ("Nigeria", "Which festival celebrates fishing in Argungu?", "Argungu Fishing Festival", "Eyo Festival", "Durbar", "Ofala", "a", "The Argungu Fishing Festival is held in Kebbi State."),
    ("Nigeria", "What does the Durbar festival often feature?", "Horse parades", "Ice skating", "Boat racing", "Snow sculpture", "a", "Durbar celebrations often include decorated horses and traditional regalia."),
    ("Nigeria", "Which musical style is linked with Fela Kuti?", "Afrobeat", "Bluegrass", "Opera", "K-pop", "a", "Fela Kuti helped develop Afrobeat."),
    ("Nigeria", "What is a common sign of respect to elders in many Nigerian cultures?", "Ignoring greetings", "Greeting properly", "Leaving silently", "Pointing fingers", "b", "Respectful greetings are important in many Nigerian communities."),
    ("Nigeria", "Which language is widely spoken in northern Nigeria?", "Hausa", "Swedish", "Thai", "Italian", "a", "Hausa is widely spoken in northern Nigeria."),
    ("Nigeria", "Which dish is made from pounded yam and soup?", "Pounded yam with egusi", "Sushi", "Tacos", "Pho", "a", "Pounded yam is commonly eaten with soups such as egusi."),
    ("Nigeria", "What is Ankara used for?", "Traditional clothing", "Building roads", "Writing exams", "Charging phones", "a", "Ankara fabric is widely used for clothing and fashion."),
    ("Nigeria", "What does cultural storytelling help preserve?", "Heritage and values", "Passwords", "Traffic lights", "Computer cables", "a", "Stories pass cultural values and memory between generations."),
    ("Japan", "What is Hanami?", "Cherry blossom viewing", "Tea farming only", "Mountain mining", "Winter fishing", "a", "Hanami is the custom of appreciating cherry blossoms."),
    ("Japan", "Which clothing item is traditional in Japan?", "Kimono", "Poncho", "Kilt", "Sombrero", "a", "The kimono is a traditional Japanese garment."),
    ("Japan", "What is sushi usually associated with?", "Vinegared rice", "Cassava flour", "Corn dough", "Millet porridge", "a", "Sushi is based on vinegared rice with different toppings or fillings."),
    ("Japan", "Which practice is linked with matcha?", "Tea ceremony", "Harvest parade", "Mask carving", "Horse racing", "a", "Matcha is central to Japanese tea ceremony traditions."),
    ("Japan", "What does bowing usually show?", "Respect", "Anger", "Confusion only", "Disinterest", "a", "Bowing is commonly used to show respect and greeting."),
    ("Japan", "Which festival period honors ancestral spirits?", "Obon", "Carnival", "Diwali", "Thanksgiving", "a", "Obon honors ancestors and family remembrance."),
    ("Japan", "What is origami?", "Paper folding", "Pottery baking", "Drum carving", "Rice planting", "a", "Origami is the art of paper folding."),
    ("Japan", "Which food is a noodle soup?", "Ramen", "Paella", "Fufu", "Pierogi", "a", "Ramen is a Japanese noodle soup."),
    ("Japan", "What is calligraphy called in Japanese culture?", "Shodo", "Samba", "Henna", "Griot", "a", "Shodo is Japanese calligraphy."),
    ("Japan", "Which value is often emphasized in shared spaces?", "Cleanliness and order", "Loud arguments", "Queue jumping", "Wastefulness", "a", "Cleanliness and order are widely valued in Japanese public life."),
    ("Brazil", "What is Carnival famous for in Brazil?", "Music and parades", "Snow castles", "Tea silence", "Camel racing", "a", "Brazilian Carnival is known for samba, costumes, and parades."),
    ("Brazil", "Which music and dance style is closely linked with Brazil?", "Samba", "Flamenco", "Polka", "Tango only", "a", "Samba is a major Brazilian cultural expression."),
    ("Brazil", "What language is spoken by most Brazilians?", "Portuguese", "Spanish", "French", "English", "a", "Brazil's official language is Portuguese."),
    ("Brazil", "Which martial art combines dance and music?", "Capoeira", "Judo", "Fencing", "Archery", "a", "Capoeira blends martial movement, dance, and music."),
    ("Brazil", "What is feijoada?", "A bean and meat stew", "A rice dessert", "A fish-only soup", "A bread sauce", "a", "Feijoada is a traditional bean stew."),
    ("Brazil", "Which rainforest is strongly associated with Brazil?", "Amazon", "Black Forest", "Daintree", "Congo only", "a", "A large part of the Amazon rainforest is in Brazil."),
    ("Brazil", "What sport is deeply popular in Brazil?", "Football", "Curling", "Cricket only", "Ice hockey", "a", "Football is a major part of Brazilian popular culture."),
    ("Brazil", "Which city is known for a major Carnival parade at the Sambadrome?", "Rio de Janeiro", "Tokyo", "Cairo", "Toronto", "a", "Rio de Janeiro is famous for its Carnival parades."),
    ("Brazil", "What is a berimbau used in?", "Capoeira music", "Tea ceremony", "Opera staging", "Chess tournaments", "a", "The berimbau is a musical instrument used in capoeira."),
    ("Brazil", "Which cultural value is often shown through festivals?", "Community celebration", "Isolation", "Silence only", "Avoiding music", "a", "Brazilian festivals often emphasize community and celebration."),
    ("India", "Which festival is known as the festival of lights?", "Diwali", "Obon", "Carnival", "Durbar", "a", "Diwali is widely known as the festival of lights."),
    ("India", "What is henna body art commonly called?", "Mehndi", "Origami", "Aso oke", "Capoeira", "a", "Mehndi is decorative henna art used in celebrations."),
    ("India", "Which garment is traditionally worn by many Indian women?", "Sari", "Kimono", "Kilt", "Poncho", "a", "A sari is a traditional Indian garment."),
    ("India", "What is Bollywood known for?", "Indian film and music", "Fishing festivals", "Tea farming", "Snow games", "a", "Bollywood is India's Hindi-language film industry."),
    ("India", "Which food uses many spice blends?", "Curry", "Plain ice", "Toast only", "Raw potato", "a", "Indian cooking is known for complex spice blends."),
    ("India", "What does Namaste usually express?", "Greeting and respect", "Disagreement", "Departure only", "Silence", "a", "Namaste is a respectful greeting."),
    ("India", "Which festival involves colors?", "Holi", "Obon", "Thanksgiving", "Eyo", "a", "Holi is celebrated with colors."),
    ("India", "Which classical discipline combines movement, breath, and meditation?", "Yoga", "Fencing", "Skiing", "Baseball", "a", "Yoga has deep roots in Indian tradition."),
    ("India", "What is a common Indian flatbread?", "Naan", "Sushi", "Taco shell", "Pierogi", "a", "Naan is a popular flatbread."),
    ("India", "Why is family important in many Indian communities?", "It supports identity and responsibility", "It replaces all schools", "It removes culture", "It stops festivals", "a", "Family networks often support identity, care, and responsibility."),
    ("Mexico", "What is Dia de los Muertos?", "Day of the Dead", "Festival of Ice", "Tea Day", "Fishing Day", "a", "Dia de los Muertos honors loved ones who have died."),
    ("Mexico", "Which food uses a folded or rolled tortilla?", "Taco", "Sushi", "Ramen", "Pounded yam", "a", "Tacos are made with tortillas and fillings."),
    ("Mexico", "Which music style is strongly linked with Mexico?", "Mariachi", "Afrobeat", "Samba only", "Opera only", "a", "Mariachi is a well-known Mexican music tradition."),
    ("Mexico", "What is a piñata used for?", "Celebrations and parties", "Database backup", "Tea brewing", "Formal voting", "a", "Piñatas are common in celebrations."),
    ("Mexico", "Which ancient civilization is part of Mexican heritage?", "Maya", "Viking", "Samurai", "Roman only", "a", "Maya heritage is part of Mexico's deep history."),
    ("Mexico", "What is mole?", "A rich sauce", "A dance shoe", "A hat", "A drum", "a", "Mole is a traditional sauce with many variations."),
    ("Mexico", "What do marigolds symbolize during Day of the Dead?", "Guiding spirits", "Building houses", "Making snow", "Starting exams", "a", "Marigolds are used in Day of the Dead altars and symbolism."),
    ("Mexico", "What is papel picado?", "Decorative cut paper", "A rice dish", "A shoe style", "A quiz rule", "a", "Papel picado is decorative cut paper used for celebrations."),
    ("Mexico", "Which language is spoken by most Mexicans?", "Spanish", "Japanese", "Hindi", "Yoruba only", "a", "Spanish is the main language spoken in Mexico."),
    ("Mexico", "What does sharing food often support?", "Community and hospitality", "SQL injection", "Network failure", "File deletion", "a", "Food traditions often strengthen hospitality and community."),
]


def init_db():
    with DBConnection.cursor(commit=True, dict_cursor=False) as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password_hash VARCHAR(256) NOT NULL,
                country VARCHAR(100),
                bio TEXT,
                avatar_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS posts (
                post_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                category VARCHAR(50) NOT NULL CHECK (category IN ('Food', 'Festival', 'Music', 'Custom')),
                image_path VARCHAR(255),
                country VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS comments (
                comment_id SERIAL PRIMARY KEY,
                post_id INTEGER NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                content TEXT NOT NULL,
                flagged BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS quiz_questions (
                q_id SERIAL PRIMARY KEY,
                country VARCHAR(100) NOT NULL,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_option CHAR(1) NOT NULL CHECK (correct_option IN ('a', 'b', 'c', 'd')),
                explanation TEXT,
                UNIQUE(country, question)
            );

            CREATE TABLE IF NOT EXISTS quiz_scores (
                score_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                country VARCHAR(100),
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL DEFAULT 5,
                percentage INTEGER NOT NULL DEFAULT 0,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_posts_country ON posts(country);
            CREATE INDEX IF NOT EXISTS idx_posts_category ON posts(category);
            CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
            CREATE INDEX IF NOT EXISTS idx_quiz_questions_country ON quiz_questions(country);
            """
        )

    seed_quiz_questions()


def seed_quiz_questions():
    with DBConnection.cursor(commit=True, dict_cursor=False) as cur:
        cur.executemany(
            """
            INSERT INTO quiz_questions (
                country, question, option_a, option_b, option_c, option_d,
                correct_option, explanation
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (country, question) DO NOTHING;
            """,
            QUIZ_SEED,
        )


if __name__ == "__main__":
    init_db()
    print("CultureBridge database tables and seed data are ready.")

