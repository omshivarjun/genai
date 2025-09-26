const newTaskInput = document.getElementById("new-task");
const addTaskButton = document.getElementById("add-task");
const taskList = document.getElementById("task-list");

function addTask() {
  const taskText = newTaskInput.value.trim();

  if (taskText !== "") {
    const listItem = document.createElement("li");
    listItem.textContent = taskText;

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.classList.add("delete-button");
    listItem.appendChild(deleteButton);

    deleteButton.addEventListener("click", function() {
      listItem.remove();
    });

    listItem.addEventListener("click", function() {
      listItem.classList.toggle("completed");
    });

    taskList.appendChild(listItem);
    newTaskInput.value = "";
  }
}

addTaskButton.addEventListener("click", addTask);
