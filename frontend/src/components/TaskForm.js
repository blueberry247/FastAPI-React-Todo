const TaskForm = ({ value, onChange, onSubmit }) => {
  return (
    <form className="w-full" onSubmit={onSubmit}>
      <input
        autoFocus
        className="w-full rounded border border-gray-300 p-3 outline-none focus:border-pink-500"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Type a task and press Enter"
      />
    </form>
  );
};

export default TaskForm;
