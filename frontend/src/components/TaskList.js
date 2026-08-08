import SubTaskItem from "./SubTaskList";

const TaskList = ({ tasks, onToggle, onUpdateContent, onDelete }) => {
  if (tasks.length === 0) {
    return <p className="py-10 text-center text-gray-500">No tasks yet. Add one above.</p>;
  }

  return (
    <ul className="mx-auto max-w-2xl p-5">
      {tasks.map((task) => (
        <SubTaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onUpdateContent={onUpdateContent}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
};

export default TaskList;
