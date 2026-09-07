import pandas as pd
import random

data = []

for i in range(500):

    cgpa = round(random.uniform(5.0, 9.5), 2)
    aptitude = random.randint(40, 95)
    technical_skills = random.randint(2, 10)
    internships = random.randint(0, 3)
    projects = random.randint(0, 5)
    communication = random.randint(4, 10)
    backlogs = random.randint(0, 3)
    certifications = random.randint(0, 5)

    # Calculate placement score
    score = (
        cgpa * 10
        + aptitude * 0.3
        + technical_skills * 4
        + internships * 5
        + projects * 3
        + communication * 3
        + certifications * 2
        - backlogs * 8
    )

    # Placement decision
    if score >= 150:
        placed = 1
    else:
        placed = 0

    data.append([
        cgpa,
        aptitude,
        technical_skills,
        internships,
        projects,
        communication,
        backlogs,
        certifications,
        placed
    ])


# Create DataFrame
columns = [
    "cgpa",
    "aptitude_score",
    "technical_skills",
    "internships",
    "projects",
    "communication_score",
    "backlogs",
    "certifications",
    "placed"
]

df = pd.DataFrame(data, columns=columns)

# Save dataset
df.to_csv("placement_data.csv", index=False)

print("Dataset generated successfully!")
print("Total students:", len(df))
print("Dataset saved as placement_data.csv")