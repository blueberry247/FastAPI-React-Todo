import { useEffect, useState } from "react";

import apiRequest from "../CRUD utils/apiRequest";
import TaskForm from "./TaskForm";
import TaskList from "./TaskList";

const API_USER_ID = 1;

const MainMenu = () => {
  const [tasks, setTasks] = useState([]);
  const [newTaskText, setNewTaskText] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load tasks once when the page opens.
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setIsLoading(true);
      const data = await apiRequest("/items/");
      setTasks(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const createTask = async (event) => {
    event.preventDefault();

    const content = newTaskText.trim();
    if (!content) return;

    try {
      const createdTask = await apiRequest(`/users/${API_USER_ID}/items/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, is_active: true }),
      });

      setTasks([...tasks, createdTask]);
      setNewTaskText("");
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const saveTask = async (updatedTask) => {
    const savedTask = await apiRequest(`/items/${updatedTask.id}/`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content: updatedTask.content,
        is_active: updatedTask.is_active,
      }),
    });

    setTasks(tasks.map((task) => (task.id === savedTask.id ? savedTask : task)));
  };

  const toggleTask = async (task) => {
    try {
      await saveTask({ ...task, is_active: !task.is_active });
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const updateTaskContent = async (task, content) => {
    const updatedTask = { ...task, content };

    // Update the UI immediately so typing feels responsive.
    setTasks(tasks.map((item) => (item.id === task.id ? updatedTask : item)));

    try {
      await saveTask(updatedTask);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await apiRequest(`/items/${taskId}/`, { method: "DELETE" });
      setTasks(tasks.filter((task) => task.id !== taskId));
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b-4 border-black bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <h1 className="text-xl font-bold">FastAPI + React ToDo</h1>
          <a className="font-medium text-pink-500" href="/docs" target="_blank" rel="noreferrer">
            API Docs
          </a>
        </div>
      </header>

      <section className="sticky top-0 bg-pink-500 p-4">
        <div className="mx-auto max-w-2xl rounded bg-white p-3">
          <TaskForm value={newTaskText} onChange={setNewTaskText} onSubmit={createTask} />
        </div>
      </section>

      <main>
        {isLoading && <p className="p-10 text-center text-pink-500">Loading tasks...</p>}
        {error && <p className="p-10 text-center text-red-600">Error: {error}</p>}
        {!isLoading && !error && (
          <TaskList
            tasks={tasks}
            onToggle={toggleTask}
            onUpdateContent={updateTaskContent}
            onDelete={deleteTask}
          />
        )}
      </main>
    </div>
  );
};

export default MainMenu;
