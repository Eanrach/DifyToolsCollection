import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import os
import json
import tempfile
import zipfile
import io
from datetime import datetime

def create_files_from_structure(structure: str) -> dict:
    """
    根据提供的文件结构创建目录和文件，并返回zip压缩包
    
    Args:
        structure: 包含文件结构的数组对象
        
    Returns:
        dict: 包含zip文件数据的字典
    """
    try:
        # 解析输入参数
        if not structure or not isinstance(structure, str):
            return {
                "error": "Invalid input",
                "details": "Structure must be a string"
            }
        
        # 字符串转JSON
        structure = json.loads(structure)

        file_structure = []
        files_data = []
        
        for item in structure["files"]:
            files_data.append(item)
            file_structure.append(item["filename"])

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 确保所有文件都存在于 file_structure 中
            for file_data in files_data:
                filename = file_data.get('filename')
                if filename and filename not in file_structure:
                    file_structure.append(filename)
            
            # 创建目录结构
            created_files = []
            for file_path in file_structure:
                full_path = temp_path / file_path
                
                # 创建父目录
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 查找文件内容
                content = None
                for file_data in files_data:
                    if file_data.get('filename') == file_path:
                        content = file_data.get('content', '')
                        break
                
                # 写入文件内容
                if content is not None:
                    full_path.write_text(content, encoding='utf-8')
                    created_files.append(str(full_path))
                else:
                    # 如果没有内容，创建空文件
                    full_path.touch()
                    created_files.append(str(full_path))
            
            # 创建zip文件
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_file.write(file_path, arcname)
            
            zip_buffer.seek(0)
            zip_data = zip_buffer.read()
            
            # 创建结果信息
            result_info = {
                "total_files": len(created_files),
                "created_files": created_files,
                "file_structure": file_structure,
                "timestamp": datetime.now().isoformat()
            }
            
            return {
                "result": result_info,
                "file": {
                    "data": zip_data,
                    "mime_type": "application/zip",
                    "filename": f"created_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                }
            }
            
    except Exception as e:
        return {
            "error": "Failed to create files",
            "details": str(e)
        }

# a = "{\\n  \\"file_structure\\": [\\n    \\"ChannelTuner.toc\\",\\n    \\"ChannelTuner.lua\\",\\n    \\"Config.lua\\",\\n    \\"UI.lua\\",\\n    \\"SoundList.lua\\",\\n    \\"Localization.lua\\"\\n  ],\\n  \\"files\\": [\\n    {\\n      \\"filename\\": \\"ChannelTuner.toc\\",\\n      \\"content\\": \\"## Interface: 100100\\\\n## Title: ChannelTuner\\\\n## Notes: 为聊天频道定制声音提醒\\\\n## Author: YourName\\\\n## Version: 1.0.0\\\\n## SavedVariables: ChannelTunerDB\\\\n\\\\nChannelTuner.lua\\\\nConfig.lua\\\\nUI.lua\\\\nSoundList.lua\\\\nLocalization.lua\\"\\n    },\\n    {\\n      \\"filename\\": \\"ChannelTuner.lua\\",\\n      \\"content\\": \\"-- 主文件\\\\nlocal addonName, addon = ...\\\\n\\\\n-- 全局变量\\\\nChannelTuner = {}\\\\nChannelTuner.db = {}\\\\nChannelTuner.sounds = {}\\\\nChannelTuner.channels = {\\\\n    \\\\\\"SAY\\\\\\",\\\\n    \\\\\\"YELL\\\\\\",\\\\n    \\\\\\"WHISPER\\\\\\",\\\\n    \\\\\\"PARTY\\\\\\",\\\\n    \\\\\\"RAID\\\\\\",\\\\n    \\\\\\"GUILD\\\\\\",\\\\n    \\\\\\"OFFICER\\\\\\",\\\\n    \\\\\\"CHANNEL\\\\\\",\\\\n    \\\\\\"EMOTE\\\\\\",\\\\n    \\\\\\"SYSTEM\\\\\\"\\\\n}\\\\n\\\\n-- 初始化\\\\nfunction ChannelTuner:OnInitialize()\\\\n    -- 加载配置\\\\n    self.db = ChannelTunerDB or {}\\\\n    self.sounds = ChannelTuner.sounds\\\\n    \\\\n    -- 注册指令\\\\n    self:RegisterSlashCommands()\\\\n    \\\\n    -- 设置事件监听\\\\n    self:SetupEventHandlers()\\\\n    \\\\n    -- 打印加载信息\\\\n    print(\\\\\\"|cFF00FF00ChannelTuner已加载。输入/ct或/channeltuner打开设置界面。|r\\\\\\")\\\\nend\\\\n\\\\n-- 注册斜杠指令\\\\nfunction ChannelTuner:RegisterSlashCommands()\\\\n    SLASH_CHANNELTUNER1 = \\\\\\"/channeltuner\\\\\\"\\\\n    SLASH_CHANNELTUNER2 = \\\\\\"/ct\\\\\\"\\\\n    SlashCmdList[\\\\\\"CHANNELTUNER\\\\\\"] = function(msg)\\\\n        self:ToggleUI()\\\\n    end\\\\nend\\\\n\\\\n-- 切换UI显示\\\\nfunction ChannelTuner:ToggleUI()\\\\n    if ChannelTunerFrame and ChannelTunerFrame:IsShown() then\\\\n        ChannelTunerFrame:Hide()\\\\n    else\\\\n        ChannelTunerFrame:Show()\\\\n    end\\\\nend\\\\n\\\\n-- 设置事件处理器\\\\nfunction ChannelTuner:SetupEventHandlers()\\\\n    local frame = CreateFrame(\\\\\\"Frame\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_SAY\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_YELL\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_WHISPER\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_PARTY\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_RAID\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_GUILD\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_OFFICER\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_CHANNEL\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_EMOTE\\\\\\")\\\\n    frame:RegisterEvent(\\\\\\"CHAT_MSG_SYSTEM\\\\\\")\\\\n    \\\\n    frame:SetScript(\\\\\\"OnEvent\\\\\\", function(self, event, ...)\\\\n        ChannelTuner:HandleChatEvent(event, ...)\\\\n    end)\\\\nend\\\\n\\\\n-- 处理聊天事件\\\\nfunction ChannelTuner:HandleChatEvent(event, text, player, ...)\\\\n    local channel = event:gsub(\\\\\\"CHAT_MSG_\\\\\\", \\\\\\"\\\\\\")\\\\n    local settings = self.db[channel]\\\\n    \\\\n    -- 检查是否有为该频道设置声音\\\\n    if settings and settings.enabled and settings.sound then\\\\n        -- 播放声音\\\\n        PlaySoundFile(settings.sound, \\\\\\"Master\\\\\\")\\\\n    end\\\\nend\\\\n\\\\n-- 保存设置\\\\nfunction ChannelTuner:SaveSettings(channel, settings)\\\\n    if not self.db[channel] then\\\\n        self.db[channel] = {}\\\\n    end\\\\n    \\\\n    for key, value in pairs(settings) do\\\\n        self.db[channel][key] = value\\\\n    end\\\\n    \\\\n    -- 保存到SavedVariables\\\\n    ChannelTunerDB = self.db\\\\nend\\\\n\\\\n-- 初始化插件\\\\nlocal frame = CreateFrame(\\\\\\"Frame\\\\\\")\\\\nframe:RegisterEvent(\\\\\\"ADDON_LOADED\\\\\\")\\\\nframe:SetScript(\\\\\\"OnEvent\\\\\\", function(self, event, addonLoaded)\\\\n    if addonLoaded == addonName then\\\\n        ChannelTuner:OnInitialize()\\\\n    end\\\\nend)\\"\\n    },\\n    {\\n      \\"filename\\": \\"Config.lua\\",\\n      \\"content\\": \\"-- 配置管理\\\\nlocal addonName, addon = ...\\\\n\\\\nChannelTuner.Config = {}\\\\n\\\\n-- 默认配置\\\\nlocal defaults = {\\\\n    version = 1,\\\\n    channels = {}\\\\n}\\\\n\\\\n-- 获取频道配置\\\\nfunction ChannelTuner.Config:GetChannelConfig(channel)\\\\n    if not ChannelTuner.db[channel] then\\\\n        ChannelTuner.db[channel] = {\\\\n            enabled = false,\\\\n            sound = nil,\\\\n            volume = 1.0\\\\n        }\\\\n    end\\\\n    return ChannelTuner.db[channel]\\\\nend\\\\n\\\\n-- 设置频道配置\\\\nfunction ChannelTuner.Config:SetChannelConfig(channel, config)\\\\n    ChannelTuner.db[channel] = config\\\\n    ChannelTuner:SaveSettings(channel, config)\\\\nend\\\\n\\\\n-- 获取所有频道配置\\\\nfunction ChannelTuner.Config:GetAllConfigs()\\\\n    local configs = {}\\\\n    for _, channel in ipairs(ChannelTuner.channels) do\\\\n        configs[channel] = self:GetChannelConfig(channel)\\\\n    end\\\\n    return configs\\\\nend\\\\n\\\\n-- 重置配置\\\\nfunction ChannelTuner.Config:ResetConfig()\\\\n    ChannelTuner.db = {}\\\\n    ChannelTunerDB = {}\\\\n    print(\\\\\\"|cFF00FF00ChannelTuner配置已重置。|r\\\\\\")\\\\nend\\"\\n    },\\n    {\\n      \\"filename\\": \\"UI.lua\\",\\n      \\"content\\": \\"-- 用户界面\\\\nlocal addonName, addon = ...\\\\n\\\\n-- 创建主框架\\\\nlocal frame = CreateFrame(\\\\\\"Frame\\\\\\", \\\\\\"ChannelTunerFrame\\\\\\", UIParent, \\\\\\"BasicFrameTemplate\\\\\\")\\\\nframe:SetSize(500, 600)\\\\nframe:SetPoint(\\\\\\"CENTER\\\\\\")\\\\nframe:SetMovable(true)\\\\nframe:EnableMouse(true)\\\\nframe:RegisterForDrag(\\\\\\"LeftButton\\\\\\")\\\\nframe:SetScript(\\\\\\"OnDragStart\\\\\\", frame.StartMoving)\\\\nframe:SetScript(\\\\\\"OnDragStop\\\\\\", frame.StopMovingOrSizing)\\\\nframe:Hide()\\\\n\\\\n-- 标题\\\\nframe.title = frame:CreateFontString(nil, \\\\\\"OVERLAY\\\\\\", \\\\\\"GameFontHighlight\\\\\\")\\\\nframe.title:SetPoint(\\\\\\"TOP\\\\\\", 0, -5)\\\\nframe.title:SetText(\\\\\\"ChannelTuner - 聊天频道声音设置\\\\\\")\\\\n\\\\n-- 关闭按钮\\\\nframe.closeBtn = CreateFrame(\\\\\\"Button\\\\\\", nil, frame, \\\\\\"UIPanelCloseButton\\\\\\")\\\\nframe.closeBtn:SetPoint(\\\\\\"TOPRIGHT\\\\\\", -5, -5)\\\\nframe.closeBtn:SetScript(\\\\\\"OnClick\\\\\\", function()\\\\n    frame:Hide()\\\\nend)\\\\n\\\\n-- 创建滚动框架\\\\nlocal scrollFrame = CreateFrame(\\\\\\"ScrollFrame\\\\\\", \\\\\\"ChannelTunerScrollFrame\\\\\\", frame, \\\\\\"UIPanelScrollFrameTemplate\\\\\\")\\\\nscrollFrame:SetPoint(\\\\\\"TOPLEFT\\\\\\", 10, -30)\\\\nscrollFrame:SetPoint(\\\\\\"BOTTOMRIGHT\\\\\\", -30, 40)\\\\n\\\\n-- 创建内容框架\\\\nlocal content = CreateFrame(\\\\\\"Frame\\\\\\", \\\\\\"ChannelTunerContent\\\\\\", scrollFrame)\\\\ncontent:SetSize(450, 800)\\\\nscrollFrame:SetScrollChild(content)\\\\n\\\\n-- 频道设置控件存储\\\\nframe.controls = {}\\\\n\\\\n-- 创建频道设置行\\\\nlocal function CreateChannelRow(parent, channel, yOffset)\\\\n    local row = CreateFrame(\\\\\\"Frame\\\\\\", nil, parent)\\\\n    row:SetSize(450, 40)\\\\n    row:SetPoint(\\\\\\"TOPLEFT\\\\\\", 0, yOffset)\\\\n    \\\\n    -- 频道标签\\\\n    row.label = row:CreateFontString(nil, \\\\\\"OVERLAY\\\\\\", \\\\\\"GameFontNormal\\\\\\")\\\\n    row.label:SetPoint(\\\\\\"LEFT\\\\\\", 10, 0)\\\\n    row.label:SetText(channel)\\\\n    \\\\n    -- 启用复选框\\\\n    row.checkbox = CreateFrame(\\\\\\"CheckButton\\\\\\", nil, row, \\\\\\"UICheckButtonTemplate\\\\\\")\\\\n    row.checkbox:SetPoint(\\\\\\"LEFT\\\\\\", 120, 0)\\\\n    row.checkbox:SetSize(24, 24)\\\\n    \\\\n    -- 声音下拉菜单\\\\n    row.soundDropdown = CreateFrame(\\\\\\"Button\\\\\\", nil, row, \\\\\\"UIDropDownMenuTemplate\\\\\\")\\\\n    row.soundDropdown:SetPoint(\\\\\\"LEFT\\\\\\", 170, 0)\\\\n    row.soundDropdown:SetSize(200, 32)\\\\n    \\\\n    -- 音量滑块\\\\n    row.volumeSlider = CreateFrame(\\\\\\"Slider\\\\\\", nil, row, \\\\\\"OptionsSliderTemplate\\\\\\")\\\\n    row.volumeSlider:SetPoint(\\\\\\"LEFT\\\\\\", 380, 0)\\\\n    row.volumeSlider:SetSize(60, 17)\\\\n    row.volumeSlider:SetMinMaxValues(0, 100)\\\\n    row.volumeSlider:SetValueStep(1)\\\\n    row.volumeSlider.Text:SetText(\\\\\\"100%\\\\\\")\\\\n    \\\\n    return row\\\\nend\\\\n\\\\n-- 刷新界面\\\\nfunction frame:RefreshUI()\\\\n    -- 清空现有控件\\\\n    for _, control in ipairs(self.controls) do\\\\n        control:Hide()\\\\n    end\\\\n    wipe(self.controls)\\\\n    \\\\n    -- 创建所有频道的设置行\\\\n    local yOffset = -10\\\\n    for _, channel in ipairs(ChannelTuner.channels) do\\\\n        local config = ChannelTuner.Config:GetChannelConfig(channel)\\\\n        \\\\n        local row = CreateChannelRow(content, channel, yOffset)\\\\n        \\\\n        -- 设置复选框状态\\\\n        row.checkbox:SetChecked(config.enabled)\\\\n        row.checkbox.channel = channel\\\\n        row.checkbox:SetScript(\\\\\\"OnClick\\\\\\", function(self)\\\\n            config.enabled = self:GetChecked()\\\\n            ChannelTuner.Config:SetChannelConfig(channel, config)\\\\n        end)\\\\n        \\\\n        -- 设置声音下拉菜单\\\\n        UIDropDownMenu_SetWidth(row.soundDropdown, 180)\\\\n        UIDropDownMenu_Initialize(row.soundDropdown, function(self, level)\\\\n            local info = UIDropDownMenu_CreateInfo()\\\\n            info.func = function(button)\\\\n                config.sound = button.value\\\\n                ChannelTuner.Config:SetChannelConfig(channel, config)\\\\n                UIDropDownMenu_SetText(row.soundDropdown, button.text)\\\\n            end\\\\n            \\\\n            -- 添加无声音选项\\\\n            info.text = \\\\\\"无\\\\\\"\\\\n            info.value = nil\\\\n            info.checked = (config.sound == nil)\\\\n            UIDropDownMenu_AddButton(info)\\\\n            \\\\n            -- 添加所有声音选项\\\\n            for name, path in pairs(ChannelTuner.sounds) do\\\\n                info.text = name\\\\n                info.value = path\\\\n                info.checked = (config.sound == path)\\\\n                UIDropDownMenu_AddButton(info)\\\\n            end\\\\n        end)\\\\n        \\\\n        -- 设置当前选择的声音\\\\n        if config.sound then\\\\n            for name, path in pairs(ChannelTuner.sounds) do\\\\n                if path == config.sound then\\\\n                    UIDropDownMenu_SetText(row.soundDropdown, name)\\\\n                    break\\\\n                end\\\\n            end\\\\n        else\\\\n            UIDropDownMenu_SetText(row.soundDropdown, \\\\\\"无\\\\\\")\\\\n        end\\\\n        \\\\n        -- 设置音量滑块\\\\n        row.volumeSlider:SetValue(config.volume * 100)\\\\n        row.volumeSlider.channel = channel\\\\n        row.volumeSlider:SetScript(\\\\\\"OnValueChanged\\\\\\", function(self, value)\\\\n            config.volume = value / 100\\\\n            self.Text:SetText(string.format(\\\\\\"%d%%\\\\\\", value))\\\\n            ChannelTuner.Config:SetChannelConfig(channel, config)\\\\n        end)\\\\n        \\\\n        table.insert(self.controls, row)\\\\n        yOffset = yOffset - 45\\\\n    end\\\\nend\\\\n\\\\n-- 测试按钮\\\\nlocal testBtn = CreateFrame(\\\\\\"Button\\\\\\", nil, frame, \\\\\\"UIPanelButtonTemplate\\\\\\")\\\\ntestBtn:SetSize(100, 30)\\\\ntestBtn:SetPoint(\\\\\\"BOTTOMLEFT\\\\\\", 10, 10)\\\\ntestBtn:SetText(\\\\\\"测试声音\\\\\\")\\\\ntestBtn:SetScript(\\\\\\"OnClick\\\\\\", function()\\\\n    PlaySoundFile(131273, \\\\\\"Master\\\\\\") -- 使用一个内置声音\\\\nend)\\\\n\\\\n-- 重置按钮\\\\nlocal resetBtn = CreateFrame(\\\\\\"Button\\\\\\", nil, frame, \\\\\\"UIPanelButtonTemplate\\\\\\")\\\\nresetBtn:SetSize(100, 30)\\\\nresetBtn:SetPoint(\\\\\\"BOTTOMRIGHT\\\\\\", -10, 10)\\\\nresetBtn:SetText(\\\\\\"重置配置\\\\\\")\\\\nresetBtn:SetScript(\\\\\\"OnClick\\\\\\", function()\\\\n    StaticPopup_Show(\\\\\\"CHANNELTUNER_RESET_CONFIRM\\\\\\")\\\\nend)\\\\n\\\\n-- 重置确认对话框\\\\nStaticPopupDialogs[\\\\\\"CHANNELTUNER_RESET_CONFIRM\\\\\\"] = {\\\\n    text = \\\\\\"确定要重置所有设置吗？\\\\\\",\\\\n    button1 = \\\\\\"确定\\\\\\",\\\\n    button2 = \\\\\\"取消\\\\\\",\\\\n    OnAccept = function()\\\\n        ChannelTuner.Config:ResetConfig()\\\\n        frame:RefreshUI()\\\\n    end,\\\\n    timeout = 0,\\\\n    whileDead = true,\\\\n    hideOnEscape = true,\\\\n}\\\\n\\\\n-- 显示时刷新界面\\\\nframe:SetScript(\\\\\\"OnShow\\\\\\", function()\\\\n    frame:RefreshUI()\\\\nend)\\\\n\\\\n-- 将帧引用存储到全局\\\\nChannelTuner.frame = frame\\"\\n    },\\n    {\\n      \\"filename\\": \\"SoundList.lua\\",\\n      \\"content\\": \\"-- 声音列表\\\\nChannelTuner.sounds = {\\\\n    -- 游戏内置声音\\\\n    [\\\\\\"金币掉落\\\\\\"] = \\\\\\"Sound\\\\\\\\\\\\\\\\Interface\\\\\\\\\\\\\\\\AuctionWindowOpen.ogg\\\\\\",\\\\n    [\\\\\\"新邮件\\\\\\"] = \\\\\\"Sound\\\\\\\\\\\\\\\\Interface\\\\\\\\\\\\\\\\IgPlayerInvite.ogg\\\\\\",\\\\n    [\\\\\\"成就获得\\\\\\"] = \\\\\\"Sound\\\\\\\\\\\\\\\\Interface\\\\\\\\\\\\\\\\LevelUp.ogg\\\\\\",\\\\n    [\\\\\\"错误提示\\\\\\"] = \\\\\\"Sound\\\\\\\\\\\\\\\\Interface\\\\\\\\\\\\\\\\Error.ogg\\\\\\",\\\\n    [\\\\\\"任务完成\\\\\\"] = \\\\\\"Sound\\\\\\\\\\\\\\\\Interface\\\\\\\\\\\\\\\\RaidWarning.ogg\\\\\\",\\\\n    [\\\\\\"升级音效\\\\\\"] = \\\\\\"Sound\\\\\\\\\\\\\\\\Interface\\\\\\\\\\\\\\\\UI_ChallengesNewRecord.ogg\\\\\\",\\\\n    [\\\\\\"拾取物品\\\\\\"] = \\\\\\"Sound\\\\\\\\\\\\\\\\Interface\\\\\\\\\\\\\\\\iPickUpCoin.ogg\\\\\\",\\\\n    \\\\n    -- 自定义声音路径示例（用户可以将自己的声音文件放入插件目录的Sounds文件夹）\\\\n    [\\\\\\"自定义1\\\\\\"] = \\\\\\"Interface\\\\\\\\\\\\\\\\AddOns\\\\\\\\\\\\\\\\ChannelTuner\\\\\\\\\\\\\\\\Sounds\\\\\\\\\\\\\\\\custom1.ogg\\\\\\",\\\\n    [\\\\\\"自定义2\\\\\\"] = \\\\\\"Interface\\\\\\\\\\\\\\\\AddOns\\\\\\\\\\\\\\\\ChannelTuner\\\\\\\\\\\\\\\\Sounds\\\\\\\\\\\\\\\\custom2.ogg\\\\\\",\\\\n    [\\\\\\"自定义3\\\\\\"] = \\\\\\"Interface\\\\\\\\\\\\\\\\AddOns\\\\\\\\\\\\\\\\ChannelTuner\\\\\\\\\\\\\\\\Sounds\\\\\\\\\\\\\\\\custom3.ogg\\\\\\",\\\\n}\\\\n\\\\n-- 获取声音列表函数\\\\nfunction ChannelTuner:GetSoundList()\\\\n    return self.sounds\\\\nend\\\\n\\\\n-- 添加自定义声音\\\\nfunction ChannelTuner:AddCustomSound(name, path)\\\\n    self.sounds[name] = path\\\\nend\\\\n\\\\n-- 移除自定义声音\\\\nfunction ChannelTuner:RemoveCustomSound(name)\\\\n    self.sounds[name] = nil\\\\nend\\"\\n    },\\n    {\\n      \\"filename\\": \\"Localization.lua\\",\\n      \\"content\\": \\"-- 本地化文件（支持多语言）\\\\nChannelTuner.L = {}\\\\n\\\\n-- 英文（默认）\\\\nChannelTuner.L[\\\\\\"enUS\\\\\\"] = {\\\\n    [\\\\\\"ADDON_LOADED\\\\\\"] = \\\\\\"ChannelTuner loaded. Type /ct or /channeltuner to open settings.\\\\\\",\\\\n    [\\\\\\"CHANNEL_SETTINGS\\\\\\"] = \\\\\\"Channel Settings\\\\\\",\\\\n    [\\\\\\"ENABLE_SOUND\\\\\\"] = \\\\\\"Enable Sound\\\\\\",\\\\n    [\\\\\\"SELECT_SOUND\\\\\\"] = \\\\\\"Select Sound\\\\\\",\\\\n    [\\\\\\"VOLUME\\\\\\"] = \\\\\\"Volume\\\\\\",\\\\n    [\\\\\\"TEST_SOUND\\\\\\"] = \\\\\\"Test Sound\\\\\\",\\\\n    [\\\\\\"RESET_SETTINGS\\\\\\"] = \\\\\\"Reset Settings\\\\\\",\\\\n    [\\\\\\"RESET_CONFIRM\\\\\\"] = \\\\\\"Are you sure you want to reset all settings?\\\\\\",\\\\n}\\\\n\\\\n-- 简体中文\\\\nChannelTuner.L[\\\\\\"zhCN\\\\\\"] = {\\\\n    [\\\\\\"ADDON_LOADED\\\\\\"] = \\\\\\"ChannelTuner 已加载。输入 /ct 或 /channeltuner 打开设置界面。\\\\\\",\\\\n    [\\\\\\"CHANNEL_SETTINGS\\\\\\"] = \\\\\\"频道设置\\\\\\",\\\\n    [\\\\\\"ENABLE_SOUND\\\\\\"] = \\\\\\"启用声音\\\\\\",\\\\n    [\\\\\\"SELECT_SOUND\\\\\\"] = \\\\\\"选择声音\\\\\\",\\\\n    [\\\\\\"VOLUME\\\\\\"] = \\\\\\"音量\\\\\\",\\\\n    [\\\\\\"TEST_SOUND\\\\\\"] = \\\\\\"测试声音\\\\\\",\\\\n    [\\\\\\"RESET_SETTINGS\\\\\\"] = \\\\\\"重置设置\\\\\\",\\\\n    [\\\\\\"RESET_CONFIRM\\\\\\"] = \\\\\\"确定要重置所有设置吗？\\\\\\",\\\\n}\\\\n\\\\n-- 获取本地化字符串\\\\nfunction ChannelTuner:GetLocaleText(key)\\\\n    local locale = GetLocale()\\\\n    local localeTable = self.L[locale] or self.L[\\\\\\"enUS\\\\\\"]\\\\n    return localeTable[key] or key\\\\nend\\"\\n    }\\n  ]\\n}"

result = create_files_from_structure(a)
print(str(result))