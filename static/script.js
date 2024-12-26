// 用來儲存所有已選擇的圖片文件名（避免重複）
let selectedImageFiles = new Set();

// 顯示選擇的 PDF 文件名稱
document.getElementById("pdf").addEventListener("change", function () {
    const pdfFileName = document.getElementById("pdf").files[0]?.name || "未選擇文件";
    document.getElementById("pdfFileName").textContent = pdfFileName;
});

// 顯示已選擇的圖片文件名稱
document.getElementById("images").addEventListener("change", function () {
    const imageFileList = Array.from(document.getElementById("images").files);
    const imageFileNames = document.getElementById("imageFileNames");
    const generatePptButton = document.getElementById("generatePptButton");

    // 更新圖片文件列表到 Set
    imageFileList.forEach(file => selectedImageFiles.add(file.name));

    // 清空顯示區域並重新顯示所有文件名
    imageFileNames.innerHTML = "";
    Array.from(selectedImageFiles).forEach((fileName, index) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${index + 1}. ${fileName}`;
        imageFileNames.appendChild(listItem);
    });

    // 限制最多選擇 5 張圖片
    const maxFiles = 5;
    if (selectedImageFiles.size > maxFiles) {
        alert(`最多只能選擇 ${maxFiles} 張圖片！`);
        generatePptButton.disabled = true; // 禁用提交按鈕
    } else {
        generatePptButton.disabled = false; // 啟用提交按鈕
    }

    // 動態調整圖片列表框高度
    if (selectedImageFiles.size > 3) {
        imageFileNames.style.maxHeight = "150px"; // 增加滾動高度
    } else {
        imageFileNames.style.maxHeight = "auto"; // 自動高度
    }
});

// 啟動進度條動畫
function startProgressBar() {
    const progressBar = document.querySelector(".progress");
    let width = 0;
    progressBar.style.width = width + "%";

    const interval = setInterval(() => {
        if (width >= 90) {
            clearInterval(interval); // 避免超過 90%
        } else {
            width += Math.random() * 10; // 模擬進度增長
            progressBar.style.width = width + "%";
        }
    }, 500);

    return interval; // 返回 interval ID，方便後續清除
}

document.getElementById("pptForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    // 顯示進度條
    const progressBarContainer = document.getElementById("progressBarContainer");
    progressBarContainer.style.display = "block";

    const formData = new FormData(this);

    try {
        const response = await fetch('/generate_ppt', { method: 'POST', body: formData });

        if (!response.ok) {
            throw new Error("生成 PPT 或問答時出錯！");
        }

        const data = await response.json();

        // 隱藏進度條
        progressBarContainer.style.display = "none";

        // 顯示 PPT 預覽
        const pptPreviewContainer = document.getElementById("pptPreviewContainer");
        pptPreviewContainer.style.display = "block";
        const pptIframe = document.getElementById("pptIframe");
        pptIframe.src = data.ppt_url;

        // 設置下載按鈕
        const downloadButton = document.getElementById("downloadPptButton");
        downloadButton.style.display = "block";
        downloadButton.replaceWith(downloadButton.cloneNode(true)); // 避免多次綁定事件
        const newDownloadButton = document.getElementById("downloadPptButton");
        newDownloadButton.addEventListener("click", function () {
            const link = document.createElement("a");
            link.href = data.ppt_url; // 後端返回的 PPT URL
            link.download = "Your_Presentation.pptx"; // 自定義下載文件名
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });


        // 顯示教授問答卡片
        const questionsContainer = document.getElementById("questionsContainer");
        questionsContainer.style.display = "block";

        const qaCards = document.getElementById("qaCards");
        qaCards.innerHTML = ""; // 清空舊的卡片
        if (data.questions && typeof data.questions === "string") {
            const questions = data.questions.split("\n").filter(q => q.trim() !== "");
            questions.forEach((question, index) => {
                const card = document.createElement("div");
                card.className = "card";
                card.innerHTML = `
                    <div class="card-inner">
                        <div class="card-front">
                            <p>${index + 1}. ${question}</p>
                        </div>
                        <div class="card-back">
                            <p>這是答案的地方（目前未實現）</p>
                        </div>
                    </div>
                `;
                qaCards.appendChild(card);
            });
        }
    } catch (error) {
        progressBarContainer.style.display = "none";
        alert(error.message);
    }
});


