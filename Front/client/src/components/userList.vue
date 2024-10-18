<template>
  <div>
    <h1>Users</h1>
    <button @click="showCreateModal = true">Create User</button>
    <modal v-if="showCreateModal" @close="showCreateModal = false">
      <form @submit.prevent="createUser">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="newUser.username" required />

        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="newUser.password"
          required
        />

        <label for="roles">Roles:</label>
        <div v-for="role in roles" :key="role">
          <label :for="role">{{ role }}</label>
          <input
            type="checkbox"
            :id="role"
            :value="role"
            v-model="newUser.roles"
          />
        </div>

        <label for="timezone">Timezone:</label>
        <input
          type="text"
          id="timezone"
          v-model="newUser.preferences.timezone"
          required
        />

        <label for="active">Is Active?</label>
        <input type="checkbox" id="active" v-model="newUser.active" />

        <button type="submit">Submit</button>
      </form>
    </modal>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Timezone</th>
          <th>Active</th>
          <th>Roles</th>
          <th>Created At</th>
          <th>Last Updated At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user._id">
          <td>{{ user._id }}</td>
          <td>
            <router-link
              :to="{ name: 'UserDetail', params: { id: user._id } }"
              >{{ user.username }}</router-link
            >
          </td>
          <td>{{ user.preferences.timezone }}</td>
          <td>{{ user.active ? "Yes" : "No" }}</td>
          <td>
            {{ user.roles ? user.roles.join(", ") : "No roles assigned" }}
          </td>
          <td>{{ formatDate(user.created_at) }}</td>
          <td>{{ formatDate(user.last_updated_at) }}</td>
          <td>
            <button @click="openEditModal(user)">Edit</button>
            <button @click="deleteUser(user._id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <modal v-if="showEditModal" @close="showEditModal = false">
      <form @submit.prevent="editUser">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="newUser.username" required />

        <label for="password">Password:</label>
        <input type="password" id="password" v-model="newUser.password" />

        <label for="roles">Roles:</label>
        <div v-for="role in roles" :key="role">
          <label :for="role">{{ role }}</label>
          <input
            type="checkbox"
            :id="role"
            :value="role"
            v-model="newUser.roles"
          />
        </div>

        <label for="timezone">Timezone:</label>
        <input
          type="text"
          id="timezone"
          v-model="newUser.preferences.timezone"
        />

        <label for="active">Is Active?</label>
        <input type="checkbox" id="active" v-model="newUser.active" />

        <button type="submit">Submit</button>
      </form>
    </modal>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      roles: ["Admin", "Manager", "Tester"],
      users: [], // Lista de usuarios obtenida del servidor
      showEditModal: false, // Control de visibilidad del modal de edición
      showCreateModal: false, // Control de visibilidad del modal de creación
      newUser: {
        _id: "",
        username: "",
        password: "",
        active: false,
        roles: [], // Roles seleccionados para el usuario
        preferences: {
          timezone: "", // Zona horaria del usuario
        },
        created_at: new Date(),
        last_updated_at: new Date(),
      },
    };
  },
  methods: {
    // Método para obtener los usuarios del servidor
    async fetchUsers() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/users");
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },

    // Método para eliminar un usuario
    async deleteUser(id) {
      try {
        await axios.delete(`http://127.0.0.1:5000/users/${id}`);
        this.fetchUsers(); // Recargar la lista de usuarios después de la eliminación
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    },

    // Método para crear un usuario
    async createUser() {
      try {
        await axios.post("http://127.0.0.1:5000/users", {
          username: this.newUser.username,
          password: this.newUser.password,
          active: this.newUser.active,
          roles: this.newUser.roles,
          preferences: {
            timezone: this.newUser.preferences.timezone,
          },
          created_at: new Date(),
          last_updated_at: new Date(),
        });
        this.fetchUsers(); // Recargar la lista de usuarios
        this.showCreateModal = false; // Cerrar el modal de creación
      } catch (error) {
        console.error("Error creating user:", error);
      }
    },

    // Método para editar un usuario
    async editUser() {
      try {
        await axios.put(`http://127.0.0.1:5000/users/${this.newUser._id}`, {
          username: this.newUser.username,
          password: this.newUser.password,
          active: this.newUser.active,
          roles: this.newUser.roles,
          preferences: {
            timezone: this.newUser.preferences.timezone,
          },
          last_updated_at: new Date(),
        });

        this.showEditModal = false; // Cerrar el modal de edición
        this.fetchUsers(); // Recargar la lista de usuarios después de la edición
      } catch (error) {
        console.error("Error editing user:", error);
      }
    },

    // Método para abrir el modal de edición con los datos del usuario seleccionado
    openEditModal(user) {
      this.newUser = { ...user };
      this.showEditModal = true;
    },

    // Formatear roles del usuario para mostrarlos en la tabla
    formatRoles(user) {
      const roles = [];
      if (user.is_user_admin) roles.push("Admin");
      if (user.is_user_manager) roles.push("Manager");
      if (user.is_user_tester) roles.push("Tester");
      return roles.join(", ");
    },

    // Método para formatear la fecha en un formato legible
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
  },
  // Cargar la lista de usuarios cuando el componente esté montado
  mounted() {
    this.fetchUsers();
  },
};
</script>
