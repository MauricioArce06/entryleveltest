<template>
  <div>
    <h1>User Details</h1>
    <p>ID: {{ user._id }}</p>
    <p>Username: {{ user.username }}</p>
    <p>Timezone: {{ user.preferences.timezone }}</p>
    <p>Active: {{ user.active ? "Yes" : "No" }}</p>
    <p>Roles:</p>
    <ul>
      <li v-for="role in user.roles" :key="role">{{ role }}</li>
    </ul>
    <p>Created At: {{ formatDate(user.created_at) }}</p>
    <p>Last Updated At: {{ formatDate(user.last_updated_at) }}</p>
    <!-- Mostrar fecha de última actualización -->

    <!-- Botón para abrir el modal de edición -->
    <button @click="openEditModal(user)">Edit</button>

    <!-- Botón para eliminar usuario -->
    <button @click="deleteUser">Delete</button>

    <!-- Modal para editar usuario -->
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
      user: {
        _id: "",
        username: "",
        password: "",
        active: false,
        roles: [],
        preferences: {
          timezone: "",
        },
        created_at: new Date(),
        last_updated_at: new Date(),
      }, // Datos del usuario actual
      newUser: {}, // Datos temporales para la edición
      showEditModal: false, // Mostrar o no el modal de edición
    };
  },
  async created() {
    const userId = this.$route.params.id;
    try {
      const response = await axios.get(`http://127.0.0.1:5000/users/${userId}`);
      this.user = response.data;
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  },
  methods: {
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

        // Llamar de nuevo a la API para obtener el usuario actualizado
        const userId = this.newUser._id; // Obtener el ID del usuario editado
        const response = await axios.get(
          `http://127.0.0.1:5000/users/${userId}`
        );
        this.user = response.data; // Actualizar los datos del usuario

        this.showEditModal = false; // Cerrar el modal de edición
      } catch (error) {
        console.error("Error editing user:", error);
      }
    },
    openEditModal(user) {
      this.newUser = { ...user }; // Copiar datos del usuario al formulario
      this.showEditModal = true; // Mostrar el modal
    },
    async deleteUser() {
      const userId = this.$route.params.id;
      try {
        await axios.delete(`http://127.0.0.1:5000/users/${userId}`);
        // Redirigir a la lista de usuarios después de eliminar
        this.$router.push("/");
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString(); // Cambia el formato según tus necesidades
    },
  },
};
</script>
