from tenable.sc import TenableSC

# Create a Tenable.sc instance
sc = TenableSC('ip')
sc.login('stuff')

# Function to retrieve and display the permissions for a specific role
for role in sc.roles.list():
    print(role)
