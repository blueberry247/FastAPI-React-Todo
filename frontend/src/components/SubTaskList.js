const SubTaskItem = ({ task, onToggle, onUpdateContent, onDelete }) => {
  return (
    <li className="mb-4 rounded border-b-4 border-black bg-white p-4 shadow-sm hover:border-pink-500">
      <div className="flex items-center gap-4">
        <input
          className="h-5 w-5 cursor-pointer accent-pink-500"
          type="checkbox"
          checked={!task.is_active}
          onChange={() => onToggle(task)}
        />

        <input
          className={
            task.is_active
              ? "flex-1 outline-none focus:text-pink-500"
              : "flex-1 text-gray-400 line-through outline-none"
          }
          disabled={!task.is_active}
          value={task.content}
          onChange={(event) => onUpdateContent(task, event.target.value)}
        />

        <button className="font-bold text-gray-500 hover:text-pink-500" onClick={() => onDelete(task.id)}>
          Delete
        </button>
      </div>
    </li>
  );
};

export default SubTaskItem;
