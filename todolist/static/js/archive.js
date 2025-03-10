async function deleteProject(button) {
    const projectId = button.getAttribute('data-project-id');
    const url = `/project/${projectId}/delete/`;
    const method = 'DELETE';

    const success = await sendRequest(url, method);

    if (success) {
        const projectElement = document.getElementById(`project-${projectId}`);
        if (projectElement) {
            projectElement.remove();
        }
    } else {
        console.error('Failed to delete project');
    }
}

async function deleteCategory(button) {
    const categoryId = button.getAttribute('data-category-id');
    const url = `/category/${categoryId}/delete/`;
    const method = 'DELETE';

    const success = await sendRequest(url, method);

    if (success) {
        const categoryElement = document.getElementById(`category-${categoryId}`);
        if (categoryElement) {
            categoryElement.remove();
        }
    } else {
        console.error('Failed to delete category');
    }
}

function updateProject(button) {
    event.preventDefault();

    const form = button.closest(".note-form");
    const formData = new FormData(form);
    const projectId = button.getAttribute('data-project-id');

    const requestBody = JSON.stringify(Object.fromEntries(formData.entries()));

    const url = `/project/${projectId}/edit/`;
    const method = "POST";

    sendRequest(url, method, requestBody).then(data => {
        console.log(data);
        if (data && data.success) {
            location.reload();
        } else {
            console.error("Server error:", data ? data.error : "No response");
        }
    });
}

function updateCategory(button) {
    event.preventDefault();

    const form = button.closest(".note-form");
    const formData = new FormData(form);
    const categoryId = button.getAttribute('data-category-id');

    const requestBody = JSON.stringify(Object.fromEntries(formData.entries()));

    const url = `/category/${categoryId}/edit/`;
    const method = "POST";

    sendRequest(url, method, requestBody).then(data => {
        console.log(data);
        if (data && data.success) {
            location.reload();
        } else {
            console.error("Server error:", data ? data.error : "No response");
        }
    });
}
