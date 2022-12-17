import pandas as pd 
df = pd.read_csv('train.csv')

df.drop(['id','bdate','has_photo','has_mobile','occupation_name'],axis=1,inplace=True)
df.info()

def sex_apply(sex):
    if sex ==2:
        return 0 
    return 1
df['education_form'].fillna('Full-time',inplace=True)
df['sex'] = df['sex'].apply(sex_apply)
print(df['education_form'].value_counts())
#df.info()

def edu_stat_apply(edu):
    if edu == 'Undergraduate applicant':
        return 0 
    elif edu == "Student (Master's)" or edu == "Student (Bachelor's)" or edu == "Student (Specialist)":
        return 1    
    elif edu == "Alumnus (Specialist) " or edu == "Alumnus (Bachelor's)" or edu == "Alumnus (Master's)":
        return 2 
    else:
        return 3
df['education_status'] = df['education_status'].apply(edu_stat_apply)

#df.inf

def lan_apply(lan):
    if lan.find('Русский') != -1:
        return 1
    else:
        return 0
df['langs'] = df['langs'].apply(lan_apply)
print(df['langs'].value_counts())

print(df['occupation_type'].value_counts())
def occu_typ_apply(ocu):
    if ocu == 'university':
        return 1
    else:
        return 0
df['occupation_type'] = df['occupation_type'].apply(occu_typ_apply)
print(df['occupation_type'].value_counts())
df.info()