<script setup>
import { ref, onMounted } from 'vue';
import { useAuth } from '../composables/useAuth';

const { userId, userEmail, fetchProtected, logout } = useAuth();
const users = ref([]);
const message = ref('');
const isError = ref(false);
const isLoading = ref(false);

// State for editing a user
const editingUser = ref(null);
const newName = ref('');
const newEmail = ref('');
const editMessage = ref('');
const isEditLoading = ref(false);

const fetchUsers = async () => {
    isLoading.value = true;
    message.value = '';
    isError.value = false;

    try {
        const data = await fetchProtected('/api/users');
        users.value = data;
    } catch (error) {
        message.value = error.message;
        isError.value = true;
        users.value = [];
    } finally {
        isLoading.value = false;
    }
};

const openEditModal = (user) => {
    editingUser.value = user;
    newName.value = user.name;
    newEmail.value = user.email;
    editMessage.value = '';
};

const saveUserUpdate = async () => {
    isEditLoading.value = true;
    editMessage.value = '';

    const updateData = {};
    if (newName.value !== editingUser.value.name) {
        updateData.name = newName.value;
    }
    if (newEmail.value !== editingUser.value.email) {
        updateData.email = newEmail.value;
    }
    
    // Check if the user is trying to change their own email
    if (updateData.email) {
        editMessage.value = "Changing email is restricted to administrators in this simple demo.";
        isEditLoading.value = false;
        return;
    }

    if (Object.keys(updateData).length === 0) {
        editMessage.value = "No changes detected.";
        isEditLoading.value = false;
        return;
    }
    
    // Only allow name update for simplicity
    const finalUpdate = { name: newName.value };

    try {
        await fetchProtected(`/api/users/${editingUser.value.id}`, 'PUT', finalUpdate);
        editMessage.value = "User updated successfully!";
        // Refresh the list after successful update
        await fetchUsers(); 
        // Close modal
        editingUser.value = null;

    } catch (error) {
        editMessage.value = error.message;
    } finally {
        isEditLoading.value = false;
    }
};

const deleteUser = async (user_id) => {
    if (user_id !== userId.value) {
        alert("You can only delete your own account in this application.");
        return;
    }
    
    if (confirm(`Are you sure you want to delete your account (ID: ${user_id})?`)) {
        try {
            await fetchProtected(`/api/users/${user_id}`, 'DELETE');
            // Success! Log out the user and refresh
            logout(); 
            // The router guard will redirect to /login
        } catch (error) {
            message.value = `Delete Error: ${error.message}`;
            isError.value = true;
        }
    }
};


// Fetch data when the component mounts
onMounted(() => {
    fetchUsers();
});

</script>

<template>
    <div class="users-container">
        <h1>👥Users List (Protected)</h1>
        <p class="current-user-info">
            Welcome, <strong>{{ userEmail }}</strong> (ID: {{ userId }}) 
            <button @click="logout" class="logout-btn">Log Out</button>
        </p>

        <div v-if="message" :class="['message-box', { 'error': isError, 'success': !isError }]">
            {{ message }}
        </div>
        
        <div v-if="isLoading" class="loading-state">
            Loading users...
        </div>

        <table v-else class="users-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>
                        <button @click="openEditModal(user)" class="edit-btn" :disabled="user.id !== userId">
                            Edit
                        </button>
                        <button @click="deleteUser(user.id)" class="delete-btn" :disabled="user.id !== userId">
                            Delete
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <div v-if="editingUser" class="modal-overlay">
        <div class="modal-content">
            <h2>Edit User {{ editingUser.name }}</h2>
            <form @submit.prevent="saveUserUpdate" class="edit-form">
                <label for="edit-name">Name</label>
                <input id="edit-name" v-model="newName" type="text" required :disabled="isEditLoading" />

                <label for="edit-email">Email (Read Only)</label>
                <input id="edit-email" :value="editingUser.email" type="email" disabled />
                
                <div v-if="editMessage" class="edit-message">{{ editMessage }}</div>

                <div class="modal-actions">
                    <button type="submit" :disabled="isEditLoading">
                        {{ isEditLoading ? 'Saving...' : 'Save Changes' }}
                    </button>
                    <button type="button" @click="editingUser = null" class="cancel-btn">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.users-container {
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
}

.current-user-info {
    text-align: right;
    margin-bottom: 20px;
    font-size: 0.9em;
}

.logout-btn {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    margin-left: 10px;
}

.users-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.users-table th, .users-table td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}

.users-table th {
    background-color: #f2f2f2;
    font-weight: bold;
}

.edit-btn {
    background-color: #ffc107;
    color: #212529;
    border: none;
    padding: 6px 10px;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 5px;
}

.delete-btn {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 6px 10px;
    border-radius: 4px;
    cursor: pointer;
}

/* Modal Styling */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    width: 90%;
    max-width: 500px;
}

.edit-form label {
    display: block;
    margin-top: 10px;
    font-weight: bold;
}

.edit-form input {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.cancel-btn {
    background-color: #6c757d;
}

.edit-message {
    color: #dc3545;
    font-size: 0.9em;
    margin-top: 10px;
}
</style>