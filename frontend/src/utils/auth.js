import { useAuthStore } from "../store/auth"; // Adjust this based on file location
import axios from "../utils/axios"; // Adjust this based on file location
import { jwtDecode } from "jwt-decode"; // Correct import for jwt-decode

// Correct import for jwt-decode
import Cookies from "js-cookie"; // Correct import for js-cookie
import Swal from "sweetalert2"; // Correct import for sweetalert2

// Configuring global toast notifications using Swal.mixin
const Toast = Swal.mixin({
  toast: true,
  position: "top",
  showConfirmButton: false,
  timer: 1500,
  timerProgressBar: true,
});

// Function to handle user login
export const login = async (email, password) => {
  try {
    // Making a POST request to obtain user tokens
    const { data, status } = await axios.post("user/token/", {
      email,
      password,
    });

    // If the request is successful, set authentication user and display success toast
    if (status === 200) {
      setAuthUser(data.access, data.refresh);

      // Displaying a success toast notification
      Toast.fire({
        icon: "success",
        title: "Signed in successfully",
      });
    }

    // Returning data and error information
    return { data, error: null };
  } catch (error) {
    // Handling errors and returning data and error information
    return {
      data: null,
      error: error.response?.data?.detail || "Something went wrong",
    };
  }
};

// Function to handle user registration
export const register = async (full_name, email, password, password2) => {
  try {
    // Making a POST request to register a new user
    const { data } = await axios.post("user/register/", {
      full_name,
      email,
      password,
      password2,
    });

    // Logging in the newly registered user and displaying success toast
    await login(email, password);

    // Displaying a success toast notification
    Toast.fire({
      icon: "success",
      title: "Signed Up Successfully",
    });

    // Returning data and error information
    return { data, error: null };
  } catch (error) {
    // Handling errors and returning data and error information
    return {
      data: null,
      error: error.response?.data || "Something went wrong",
    };
  }
};

// Function to handle user logout
export const logout = () => {
  // Removing tokens from cookies and resetting user state
  Cookies.remove("access_token");
  Cookies.remove("refresh_token");
  useAuthStore.getState().setUser(null);

  // Displaying a success toast notification
  Toast.fire({
    icon: "success",
    title: "You have been logged out.",
  });
};

// Function to set the authenticated user on page load
export const setUser = async () => {
  // Retrieving tokens from cookies
  const accessToken = Cookies.get("access_token");
  const refreshToken = Cookies.get("refresh_token");

  // Checking if tokens are present
  if (!accessToken || !refreshToken) {
    return;
  }

  // Refresh the access token if expired; otherwise, set the authenticated user
  if (isAccessTokenExpired(accessToken)) {
    const response = await getRefreshToken(refreshToken);
    setAuthUser(response.access, response.refresh);
  } else {
    setAuthUser(accessToken, refreshToken);
  }
};

// Function to set the authenticated user and update user state
export const setAuthUser = (access_token, refresh_token) => {
  // Setting tokens in cookies with expiration dates
  Cookies.set("access_token", access_token, { expires: 1, secure: true });
  Cookies.set("refresh_token", refresh_token, { expires: 7, secure: true });

  // Decoding access token to get user information
  const user = jwtDecode(access_token) ?? null;

  // Update user state with decoded user information
  if (user) {
    useAuthStore.getState().setUser(user);
  }
  useAuthStore.getState().setLoading(false);
};

// Function to refresh the access token using the refresh token
export const getRefreshToken = async () => {
  const refresh_token = Cookies.get("refresh_token");
  const response = await axios.post("user/token/refresh/", {
    refresh: refresh_token,
  });
  return response.data;
};

// Function to check if the access token is expired
export const isAccessTokenExpired = (accessToken) => {
  try {
    const decodedToken = jwtDecode(accessToken);
    return decodedToken.exp < Date.now() / 1000;
  } catch (err) {
    return true;
  }
};
