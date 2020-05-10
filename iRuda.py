import asyncio
import discord, os, re, random, sys, time, subprocess, urllib.request
from bs4 import BeautifulSoup

app = discord.Client()

access_token = os.environ["BOT_TOKEN"]
token = access_token

@app.event
async def on_ready():
    print("이루다 봇이 다음과 같이 로그인합니다.")
    print(app.user.name)
    print(app.user.id)
    print("=====누출되지 않게 하십시오.=====")

    
    f = open("C:/iruda/log/system_log.txt", 'r', encoding="UTF8")
    log = f.read()
    f.close()

    now = time.localtime()
    now_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

# 이루다 봇 게임 하기
    messages = [f'{len(app.guilds)}개의 서버와 함께해요!', '"이루다 도움말"을 입력해요!', f'{len(app.users)}명의 사람들과 함께해요!']
    while True:
        await app.change_presence(status=discord.Status.online, activity=discord.Game(name=messages[0]))
        messages.append(messages.pop(0))
        await asyncio.sleep(10)
    
    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
    f.write(log + "\n["+now_time+"] 이루다 봇 로그인")
    f.close()

@app.event
async def on_message(message):

# 시간모듈
    now = time.localtime()

    now_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    backup_time = "%04d-%02d-%02d %02d시 %02d분 %02d초" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

# 로그 불러오기
    f = open("C:/iruda/log/system_log.txt", 'r', encoding="UTF8")
    log = f.read()
    f.close()

    f = open("C:/iruda/log/chat_log.txt", 'r', encoding="UTF8")
    clog = f.read()
    f.close()

#다 찍어버리기
    if message.content.startswith("이루다"):
        id = message.author.id
        f = open("C:/iruda/log/chat_log.txt", 'w', encoding="UTF8")
        f.write(clog + "\n["+now_time+"] ID "+str(id)+" : "+message.content)
        f.close()

# 사전 사용자 정보 불러오기 및 탐색
    id = message.author.id
    channel = message.channel
    rspd = 0
    auth = 'reg'
    f = open("C:/iruda/admin.txt", 'r')
    admin = f.read()
    f.close()

    if str(id) + "." in admin:
        auth = 'ad'

# 서버 상태 불러오기
    f = open("C:/iruda/server_status.txt", 'r')
    server_status = f.read()
    f.close()

    if not(server_status == 'operating') and id == 500251192883150859 and message.content.startswith("이루다"):
        await channel.send("`개발자 ID "+str(id)+"님, 안전모드로 진입되셨습니다.`")

    if message.content.startswith("이루다") and not(server_status == 'operating'):
        if server_status == 'checking':
            if message.content == "이루다 서버상태":
                f = open("C:/iruda/server/server_check_outline.txt", 'r', encoding="UTF8")
                server_check_outline = f.read()
                f.close()

                if server_check_outline == "None":
                    server_check_outline = "서버 점검 안내문을 불러오는데 오류가 발생했어요.\n\n이 경우, 관리자가 서버 점검 안내문을 등록하지 않았거나,\n다른 사람에 의해 악의적으로 서버 점검 안내문이 변경되었거나, 혹은 서버가 예기치 않게 중지되었을 수 있어요.\n\n*자세한 사항은 관리자의 DM을 통해 물어봐주세요."

                await channel.send("감지되는 서버의 상태는 다음과 같아요.\n```서버 상태 : 점검중\n[서버 점검 안내]\n"+server_check_outline+"```")

                f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                f.write(log + "\n["+now_time+"] ID "+str(id)+" : 서버상태조회")
                f.close()
            
            elif message.content == "이루다 서버점검해제":
                if auth == 'ad':
                    f = open("C:/iruda/server_status.txt", 'w')
                    f.write('operating')
                    f.close()

                    f = open("C:/iruda/server/server_check_outline.txt", 'w', encoding="UTF8")
                    f.write('None')
                    f.close()

                    await channel.send("관리자 <@"+str(id)+">님의 요청으로 서버점검상태가 해제 되었어요.\n서버상태정보를 바꾸는데에 성공, 아웃라인 텍스트를 무효화 시켰어요.\n```승인코드 : "+str(id)+"```")

                    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                    f.write(log + "\n["+now_time+"] ID "+str(id)+" : 서버 점검상태 해제")
                    f.close()
                else:
                    await channel.send("관리자만 이용가능한 기능이예요.\n서버 점검에대한 자세한 정보는 '이루다 서버상태'를 입력해주세요!")

                    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                    f.write(log + "\n["+now_time+"] ID "+str(id)+" : 서버 점검상태 해제시도")
                    f.close()
            elif not(id == 500251192883150859):
                await channel.send("아쉽지만, 이루다 봇 서버 점검 중에는 이루다 봇을 이용할 수 없어요ㅜ\n나중에 다시 만나요!\n\n*서버 점검에 대한 더 많은 사항을 확인하려면, '이루다 서버상태'명령어를 입력해주세요.")

        else:
            if not(message.content == "이루다 서버상태초기화" and auth == "ad"):
                await channel.send("현재, 이루다 봇의 서버가 불안정하므로, 이루다 봇을 이용하실 수 없어요.\n```오류 : 지원되지 않는 서버상태코드입니다.\n서버상태코드 : "+server_status+"```\n악의적으로 서버가 예기치 않게 중단된 경우일 수 있으니 관리자에게 제보해 주세요.")
            else:
                f = open("C:/iruda/server_status.txt", 'w')
                f.write("operating")
                f.close()

                f = open("C:/iruda/server/server_check_outline.txt", 'w')
                f.write("None")
                f.close()

                await channel.send("관리자 <@"+str(id)+">님의 요청으로 서버상태를 초기화, 아웃라인 텍스트를 무효화시키는데 성공했어요.\n```승인코드 : "+str(id)+"```")

                f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                f.write(log + "\n["+now_time+"] ID "+str(id)+" : 서버 상태 초기화")
                f.close()
        if not(id == 500251192883150859) or not(server_status == 'operating' or server_status == 'checking'):
            return None


# 입구컷
    warn = ''
    isWarn = 'n'
    if os.path.isfile("C:/iruda/warn/"+str(id)+".txt"):
        f = open("C:/iruda/warn/"+str(id)+".txt", 'r')
        warn = f.read()
        f.close()
        isWarn = 'y'

    if isWarn == 'y':
        if int(warn) > 3 and message.content.startswith("이루다"):
            await channel.send("다음과 같은 오류가 발생했어요.\n```Cotents of "+str(id)+".txt : \nCumulative Alerts = "+warn+"\nNote : Users who receive more than three warnings(alerts) will not have full access to all feautures.\nYou can appeal this fact to :```<@500251192883150859>")
            return None

    if message.author.bot:
        return None

# 기본명령어
    if message.content == "이루다":
        rspd = rspd + 1
        await channel.send("네, <@"+str(id)+">님! 저 여기있어요!\n당신이 있는 곳은 `#"+str(channel)+"` 이군요!")
        if auth == 'ad':
            await channel.send("```승인 ID : "+str(id)+"\n관리자로 정상식별 되었습니다.```")

    if message.content == "이루다 도움말":
        f = open("C:/iruda/help.txt", 'rt', encoding='UTF8')
        comm_help1 = f.read()
        f.close()

        f = open("C:/iruda/help2.txt", 'rt', encoding='UTF8')
        comm_help2 = f.read()
        f.close()

        await channel.send("도움말은 제가 DM으로 보내드릴테니, 확인해주세요!")

        user = app.get_user(int(id))
        await user.send("**[이루다 베타 도움말]**\n"+comm_help1)
        await user.send(comm_help2)


        rspd = rspd + 1

    if message.content == "이루다 호출":
        await channel.send("그럼 호출해볼게요!\n(안올수도 있어용...)")
        user = app.get_user(500251192883150859)
        await user.send("주인님! <@"+str(id)+">님이 호출하셨답니다!")
        await channel.send("호출했어요!")

        f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
        f.write(log + "\n["+now_time+"] ID "+str(id)+" : 개발자 호출")
        f.close()

        rspd = rspd + 1

    if message.content.startswith("이루다 따라해"):
        repeat = message.content[8:]
        await channel.send("[이루다 봇] "+str(repeat))
        rspd = rspd + 1

    if message.content == "이루다 내정보":
        rspd = rspd + 1
        my_warn = warn
        if isWarn == 'n':
            my_warn = 'No_data'
        await channel.send("다음은 사용자 <@"+str(id)+">님의 정보예요.\n```ID : "+str(id)+"\nauth : "+auth+"\nwarn : "+my_warn+"```")
        f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
        f.write(log + "\n["+now_time+"] ID "+str(id)+" : 정보 조회")
        f.close()

    if message.content == "이루다 어드민리스트":
        rspd = rspd + 1
        f = open("C:/iruda/admin.txt", 'r')
        admin = f.read()
        f.close()

        admin = admin.split(".")
        i = 0
        admin_list = ''

        while i < len(admin) - 1:
            admin_list = admin_list + "<@" + admin[i] + ">\n"
            i = i + 1
        
        await channel.send("다음은 이루다봇 어드민으로 등록되신 분들이예요.\n"+admin_list)

        f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
        f.write(log + "\n["+now_time+"] ID "+str(id)+" : 어드민 리스트 조회")
        f.close()
    
    if message.content == "이루다 공식사이트":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 공식사이트", description="다음은 이루다 봇의 공식 사이트 주소예요.\n이루다 봇에 대한 자세한 정보를 보실수도 있고, 문제사항에 대해서 문의하실수도 있어요!\n\n공식사이트 [바로가기](https://se701-2201.wixsite.com/irudabot)\n\n새롭게 바뀐 공식사이트 [미리보기](https://www.iruda.kro.kr)")
        await channel.send(embed=embed)

    if message.content.startswith("이루다 DM "):
        rspd = rspd + 1
        if message.content[7:].startswith("<@"):
            target = re.findall(r'\d+', message.content)
            target = target[0]
            target = str(target)

            await channel.send("<@"+target+">님에게 DM을 보냈어요!\n\n수신자 : <@"+str(id)+">님\n\n발신자 : <@"+target+">님\n\n내용 : "+message.content[30:]+"\n\n`위 메시지는 DM명령어 사용건에 대한 개인정보 처리방침을 따라요. 개인정보 처리방침 전문을 조회하려면, '이루다 개인정보처리방침 1'을 입력해주세요.`")
            user = app.get_user(int(target))
            await user.send("<@"+str(id)+">님이 DM을 보냈어요!\n\n수신자 : <@"+str(id)+">님\n\n발신자 : <@"+target+">님\n\n내용 : "+message.content[30:]+"\n\n`위 메시지는 DM명령어 사용건에 대한 개인정보 처리방침을 따라요. 받은 메시지에 부적절한 요소가 포함되어있거나, 개인정보 처리방침 전문을 조회하려면 '이루다 개인정보처리방침 1'을 입력해주세요.`")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : "+target+"에게 DM전송 (내용 : "+message.content[30:]+")")
            f.close()
        else:
            await channel.send("언급된 대상을 찾지 못했어요ㅜ 메세지를 다시 한번 확인해주세요!")

    if message.content == "이루다 개인정보처리방침 1":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 DM 명령어 개인정보 처리방침", description="다음은 개인정보 처리방침의 전문입니다.\n\n 이루다 봇 DM 명령어(이하 DM 명령어)를 이용할 시, 해당 메시지를 통해 전달된 사항에 대한 책임은 모두 메시지를 전한 본인에게 있으며 이루다 봇 측은 전혀 책임이 없음을 알립니다.\n**DM 명령어로 전송된 모든 메시지는 log파일에 기록되며,** 개인정보 처리방침에 동의하지 않을 시 관리자에게 문의하여 전체 채팅 log를 삭제하실 수 있습니다.\n\n[FAQ]\nQ : DM으로부터 부적절한 메시지, 폭력성, 선정적 음란물 메시지를 받았을 땐 어떻게 해야 하나요?\nA : log 파일을 조회하여 보낸 사용자의 ID를 확보하여 해당 사용자가 더이상 이루다 봇을 이용하지 못하도록 할 수 있습니다. 필요에 따라 증거자료로 남겨둘 수도 있으니, 관리자에게 문의해주시길 바랍니다.")
        await channel.send(embed=embed)

        f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
        f.write(log + "\n["+now_time+"] ID "+str(id)+" : 사용권 계약 1 조회")
        f.close()

    if message.content == "이루다 초대" or message.content == "이루다 초대코드":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 초대하기", description="이루다 봇을 초대해주셔서 감사합니다 :D\n[여기](https://discord.com/api/oauth2/authorize?client_id=679600384422969367&permissions=8&scope=bot)를 클릭하셔서 봇을 초대하세요!\n\n*초대코드에 문제가 있다고 생각하는 경우 루다#5654님에게 문의해주세요.")
        await channel.send(embed=embed)

    if message.content == "이루다 핑":
        rspd = rspd + 1
        embed = discord.Embed(title=":ping_pong: 퐁!", description=f"이루다 봇의 응답속도는 `{round(app.latency*1000)}ms`입니다.")
        await channel.send(embed=embed)

        return None

    if message.content == "이루다 시계":
        rspd = rspd + 1
        await channel.send("현재 시각을 알려드릴게요. (이루다 봇 서버 시각입니다.)\n```KST "+now_time+"```")

    if message.content.startswith("이루다 가르치기 "):
        rspd = rspd + 1
        if not("`" in message.content) and ":" in message.content and not("learn_list" in message.content) and len(message.content[9:]) <= 100:
            lrn = message.content[9:]
            lrn = lrn.split(":")

            if not(os.path.isfile("C:/iruda/learn/"+lrn[0]+".txt")):
                f = open("C:/iruda/learn/"+lrn[0]+".txt", 'w')
                f.write(lrn[1]+"`"+str(id))
                f.close()

                f = open("C:/iruda/learn/learn_list.txt", 'r')
                lrn_list = f.read()
                f.close()

                f = open("C:/iruda/learn/learn_list.txt", 'w')
                f.write(lrn_list+lrn[0]+"`")
                f.close()

                await channel.send("아하! 방금 막 `"+lrn[0]+"`(을)를 `"+lrn[1]+"`(으)로 배웠어요!\n\n`*도배성 또는 부적절한 가르치기는 경고없이 삭제될 수 있으며, 해당 내용을 등록한 사용자는 제제대상입니다.`")
            else:
                await channel.send(lrn[0]+"(은)는 이미 배운 내용이예요!")
        else:
            await channel.send("잘못된 가르치기 형식이예요.")

    if message.content.startswith("이루다 가르치기삭제 "):
        rspd = rspd + 1
        if not(message.content[11:] == ""):
            lrn = message.content[11:]

            if os.path.isfile("C:/iruda/learn/"+lrn+".txt"):
                f = open("C:/iruda/learn/"+lrn+".txt", 'r')
                lrn_info = f.read()
                f.close()

                lrn_info = lrn_info.split("`")

                if str(id) == lrn_info[1] or auth == 'ad':

                    os.remove("C:/iruda/learn/"+lrn+".txt")

                    f = open("C:/iruda/learn/learn_list.txt", 'r')
                    lrn_list = f.read()
                    f.close()

                    lrn_list = lrn_list[:lrn_list.find(lrn)] + lrn_list[lrn_list.find(lrn)+len(lrn)+1:]

                    f = open("C:/iruda/learn/learn_list.txt", 'w')
                    f.write(lrn_list)
                    f.close()

                    await channel.send("<@"+lrn_info[1]+">님이 만드신 가르치기 `"+lrn+"`(이)가 정상삭제되었어요.")
                else:
                    await channel.send("당신은 그 가르치기를 생성한 사람이 아니에요!")
            else:
                await channel.send(lrn+"(은)는 아직 배운 내용이 아니에요!")
        else:
            await channel.send("잘못된 가르치기삭제 형식이예요.")

    if message.content == "이루다 가르치기목록":
        rspd = rspd + 1
        f = open("C:/iruda/learn/learn_list.txt", 'r')
        lrn_list = f.read()
        f.close()

        lrn_list = lrn_list.split("`")
        i = 0
        learn_list = ''

        while i < len(lrn_list) - 1:
            learn_list = learn_list + "  " + lrn_list[i] + "\n"
            i = i + 1
        
        await channel.send("다음은 이루다봇이 학습한 단어의 목록이예요.\n```[학습목록]\n"+learn_list+"```")

        f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
        f.write(log + "\n["+now_time+"] ID "+str(id)+" : 어드민 리스트 조회")
        f.close()

    if message.content == "이루다 핑":
        hostname = "google.com"
        response = os.system("ping -c 1 -t "+hostname)

        await channel.send(response)


# 관리자 명령어
    if message.content.startswith("이루다 경고주기"):
        rspd = rspd + 1
        if auth == 'ad':
            if message.content[9:].startswith("<@"):
                target = re.findall(r'\d+', message.content)
                target = target[0]
                target = str(target)
                if os.path.isfile("C:/iruda/warn/"+target+".txt"):
                    f = open("C:/iruda/warn/"+target+".txt", 'r')
                    p_warn = f.read()
                    f.close()
                    n_warn = int(p_warn) + 1
                    n_warn = str(n_warn)

                    f = open("C:/iruda/warn/"+target+".txt", 'w')
                    f.write(n_warn)
                    f.close()
                    await channel.send("관리자 <@"+str(id)+">님께서,\n<@"+str(target)+">님에게 경고를 누적했어요.\n현재 경고 `1`회가 누적되어, 총 경고수가 `"+n_warn+"`회가 되었어요.")
                    
                    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                    f.write(log + "\n["+now_time+"] ID "+str(id)+" : "+target+"에게 경고누적")
                    f.close()

                    f = open("C:/iruda/admin.txt", 'r')
                    admin = f.read()
                    f.close()
                    
                    if target in admin and n_warn > '3':
                        admin.find(target)
                        admin = admin[:admin.find(target)] + admin[admin.find(target)+19:]                
                        f = open("C:/iruda/admin.txt", 'w')
                        f.write(admin)
                        f.close()
                        await channel.send("<@"+target+">님의 경고가 일정수준 이상으로 누적되어 관리자 자격을 박탈했어요.")

                        f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                        f.write(log + "\n["+now_time+"] ID "+target+" : 관리자 자격 박탈")
                        f.close()
                else:
                    f = open("C:/iruda/warn/"+target+".txt", 'w')
                    f.write("1")
                    f.close()
                    await channel.send("관리자 <@"+str(id)+">님께서,\n<@"+target+">님에게 경고를 누적했어요.\n경고 `1`회가 새로 누적되었어요.")

                    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                    f.write(log + "\n["+now_time+"] ID "+str(id)+" : "+target+"에게 경고누적")
                    f.close()
            else:
                await channel.send("언급된 대상을 찾지 못했어요...\n메시지를 확인해주세오!")
        else:
            await channel.send("이 기능은 관리자만 사용할 수 있어요.")

    if message.content.startswith("이루다 어드민추가"):
        rspd = rspd + 1
        if auth == 'ad' or id == 500251192883150859:
            if message.content[10:].startswith("<@"):
                target = re.findall(r'\d+', message.content)
                target = target[0]
                target = str(target)
                if not(target in admin):
                    f = open("C:/iruda/admin.txt", 'r')
                    admin = f.read()
                    f.close()
                    admin = admin + target + "."
                    
                    f = open("C:/iruda/admin.txt", 'w')
                    f.write(admin)
                    f.close()
                    await channel.send("관리자 <@"+str(id)+">님,\n<@"+target+">님이 관리자로 정상등록되었어요.")

                    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                    f.write(log + "\n["+now_time+"] ID "+str(id)+" : "+target+"을 어드민으로 추가")
                    f.close()
                else:
                    await channel.send("이미 <@"+target+">님은 관리자로 지정되어있는 사람이예요.")
            else:
                await channel.send("언급된 대상을 찾지 못했어요...ㅜ")
        else:
            await channel.send("너어어는... 내가 주인님한테 말해서 경고주게 할꺼야!")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : 어드민 추가 시도")
            f.close()

    if message.content.startswith("이루다 어드민해제"):
        rspd = rspd + 1
        if auth == 'ad':     
            if message.content[10:].startswith("<@"):
                target = re.findall(r'\d+', message.content)
                target = target[0]
                target = str(target)
                f = open("C:/iruda/admin.txt", 'r')
                admin = f.read()
                f.close()
                if target + "." in admin:
                    admin.find(target)
                    admin = admin[:admin.find(target)] + admin[admin.find(target)+19:]                
                    f = open("C:/iruda/admin.txt", 'w')
                    f.write(admin)
                    f.close()
                    await channel.send("관리자 <@"+str(id)+">님,\n<@"+target+">님이 관리자 목록에서 정상삭제되었어요.")

                    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                    f.write(log + "\n["+now_time+"] ID "+str(id)+" : "+target+"의 어드민 자격 박탈")
                    f.close()
                else:
                    await channel.send("제가 찾아보니, <@"+target+">님은 어드민으로 등록되어있지 않았어요.")

                    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                    f.write(log + "\n["+now_time+"] ID "+str(id)+" : "+target+"의 어드민 자격 박탈 시도")
                    f.close()
            else:
                await channel.send("언급된 대상을 찾지 못했어요...ㅜ")
        else:
            await channel.send("당신은 관리자가 아니라굿!")

    if message.content.startswith("이루다 경고해제"):
        rspd = rspd + 1        
        if auth == 'ad':
            if message.content[9:].startswith("<@"):
                target = re.findall(r'\d+', message.content)
                target = target[0]
                target = str(target)
                if os.path.isfile("C:/iruda/warn/"+target+".txt"):
                    f = open("C:/iruda/warn/"+target+".txt", 'w')
                    f.write('0')
                    f.close()
                    await channel.send("관리자 <@"+str(id)+">님께서,\n<@"+str(target)+">님의 경고를 모두 초기화 시켜주셨어요!")

                    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                    f.write(log + "\n["+now_time+"] ID "+str(id)+" : "+target+"의 경고를 모두 해제")
                    f.close()
                else:
                    await channel.send("<@"+target+">님은 경고가 누적되지 않았는걸요?")

                    f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                    f.write(log + "\n["+now_time+"] ID "+str(id)+" : "+target+"을 경고해제 시도(경고가 누적되지 않음)")
                    f.close()
            else:
                await channel.send("언급된 대상을 찾지 못했어요...\n메시지를 확인해주세오!")
        else:
            await channel.send("삑ㅡ 사용하지 마때여!")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : "+target+"을 경고해제 시도(권한이 없음)")
            f.close()

    if message.content == "이루다 꺼져":
        rspd = rspd + 1
        if auth == 'ad':
            await channel.send("네, 주인님. 알아서 잘 꺼지도록 할게요.")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : 봇 종료")
            f.close()

            sys.exit()
        else:
            await channel.send("님이 어디다 대고 꺼지라 마라세요?")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : 봇 종료시도")
            f.close()

    if message.content.startswith("이루다 서버점검설정"):
        rspd = rspd + 1
        if auth == 'ad':
            if not(message.content[11:] == ''):
                f = open("C:/iruda/server_status.txt", 'w')
                f.write('checking')
                f.close()

                f = open("C:/iruda/server/server_check_outline.txt", 'w', encoding="UTF8")
                f.write(message.content[11:])
                f.close()

                await channel.send("관리자 <@"+str(id)+">님, 서버상태정보 변경에 성공, 아웃라인 텍스트 설정을 완료했어요.\n```승인코드 : "+str(id)+"```")

                f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                f.write(log + "\n["+now_time+"] ID "+str(id)+" : 서버상태를 점검으로 변경 (아웃라인 : "+message.content[11:]+")")
                f.close()

            else:
                f = open("C:/iruda/server_status.txt", 'w')
                f.write('checking')
                f.close()

                await channel.send("관리자 <@"+str(id)+">님, 서버상태정보 변경에 성공했어요. 아웃라인 텍스트는 설정되지 않았어요.\n```승인코드 : "+str(id)+"```")

                f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                f.write(log + "\n["+now_time+"] ID "+str(id)+" : 서버상태를 점검으로 변경 (아웃라인 : 설정되지 않음)")
                f.close()
        else:
            await channel.send("관리자 이외의 사용자는 사용할 수 없는 코드예요.")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : 서버상태 점검으로 변경 시도")
            f.close()

    if message.content == "이루다 백업":
        rspd = rspd + 1
        if auth == 'ad':
            f = open("./iRuda.py", 'r', encoding="UTF8")
            backup = f.read()
            f.close()

            f = open("C:/iruda/backup/"+backup_time+"_backup.txt", 'w', encoding='UTF8')
            f.write(backup)
            f.close()

            await channel.send("소스코드가 다음과 같은 파일명으로 백업되었어요.\n`"+backup_time+"_backup.txt`")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : 소스코드 백업")
            f.close()
        else:
            await channel.send("죄송하지만, 이 명령어는 관리자만 사용할 수 있어요.")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : 소스코드 백업 시도")
            f.close()

    if message.content == "이루다 공지채널등록":
        if auth == 'ad':
            rspd = rspd + 1
            f = open("C:/iruda/notice/notice_channel.txt", 'r')
            notice_channel = f.read()
            f.close()

            if not(str(message.channel.id)+"." in notice_channel):
                f = open("C:/iruda/notice/notice_channel.txt", 'w')
                f.write(notice_channel+str(message.channel.id)+".")
                f.close()

                await channel.send("`#"+str(channel)+"`(이)가 공지 채널로 등록되었어요!")
            else:
                await channel.send("이 채널은 이미 공지채널로 등록되었어요.")
        else:
            await channel.send("당신은 이 명령어를 사용할 권한이 없어요!")

    if message.content.startswith("이루다 공지쓰기 "):
        rspd = rspd + 1
        if auth == 'ad':
            notice_content = message.content[9:]

            f = open("C:/iruda/notice/notice.txt", 'w')
            f.write(notice_content)
            f.close()
            
            f = open("C:/iruda/notice/notice_channel.txt", 'r')
            notice_channel = f.read()
            f.close()

            notice_channel = notice_channel.split(".")

            i = 0
            while i < len(notice_channel)-1:
                channel = app.get_channel(int(notice_channel[i]))
                await channel.send("**[이루다 봇 공지]**\n"+notice_content+"\n\n```ID : "+str(id)+"님이 작성하셨습니다.```")
                i = i + 1

            channel = message.channel
            await channel.send(str(len(notice_channel)-1)+"개의 공지 채널에 공지가 등록되었어요.")
        else:
            await channel.send("당신은 이 명령어를 사용할 권한이 없어요!")

    if message.content.startswith("이루다 공지채널등록해제"):
        rspd = rspd + 1
        if auth == 'ad':
            target = str(message.channel.id)
            f = open("C:/iruda/notice/notice_channel.txt", 'r')
            notice_channel = f.read()
            f.close()
            if target + "." in notice_channel:
                notice_channel.find(target)
                notice_channel = notice_channel[:notice_channel.find(target)] + notice_channel[notice_channel.find(target)+19:]                
                f = open("C:/iruda/notice/notice_channel.txt", 'w')
                f.write(notice_channel)
                f.close()

                await channel.send("공지 채널 목록에서 현재 채널이 정상적으로 삭제 되었어요.")
            else:
                await channel.send("해당 채널은 아직 공지 채널로 등록되지 않았어요.")
        else:
            await channel.send("당신은 이 명령어를 사용할 권한이 없어요!")

    if message.content == "이루다 공지조회":
        rspd = rspd + 1
        f = open("C:/iruda/notice/notice.txt", 'r')
        notice_content = f.read()
        f.close()

        await channel.send("아래는 최근 등록된 공지의 내용이예요.\n\n"+"**[이루다 봇 공지]**\n"+notice_content+"\n\n```ID : "+str(id)+"님이 작성하셨습니다.```")

# 돈 관련 명령어
    if message.content == "이루다 통장생성":
        rspd = rspd + 1
        f = open("C:/iruda/money/get_money.txt", 'r')
        get_money = f.read()
        f.close()

        if str(id) in get_money:
            await channel.send("통장은 사용권 계약 후 처음 1회에만 지급되요. 돈이 없거나, 다른 문제가 발생했을 경우\n관리자 <@500251192883150859>님에게 문의하시길 바라요.")
        else:
            await channel.send("돈 명령어 관련 기능을 사용하면 사용권 계약에 동의하는 것으로 간주되요.\n자세한 정보는 '이루다 사용권계약 1'명령어를 이용해주세요.")

            f = open("C:/iruda/money/"+str(id)+".txt", 'w')
            f.write('10000')
            f.close()
            await channel.send("돈 `10000`원이 지급되었어요.\n자신의 잔돈을 확인하시려면 '이루다 내돈'을 입력해주세요.")
            f = open("C:/iruda/money/get_money.txt", 'w')
            f.write(get_money+str(id)+".")
            f.close()

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : 통장 생성")
            f.close()

    if message.content == "이루다 사용권계약 1":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 돈 관련 명령어 최종 사용권 계약", description="사용권 계약의 정보는 다음과 같습니다.\n\n 이루다 봇 상에서 존재하는 모든 재화(이하 재화)의 가치는 없습니다. 재화를 이용한 내기, 도박과 같은 실제 화폐를 담보로 한 도박행위로 인해 발생한 피해에 대해서 이루다 봇 측에서는 아무런 책임이 없습니다. 이루다 봇은 자신의 가상계좌에 대한 돈 입금등을 가장한 협박으로부터 해당 사용자가 이루다 봇을 더이상 사용하지 못하게 할 권리가 있으며, 또한 해당 사용자를 서버에서 추방할 권리가 있습니다.\n\n[FAQ]\nQ : 사용자 계약에 동의하지 않으려면 어떻게 하야 하나요?\nA : 이루다봇의 돈 관련 명령어를 사용하지 않으시면 됩니다.\n\nQ : 이미 이루다 돈 명령어를 사용했는데, 나중에 계약을 철회하고 싶다면 어떻게 해야 하나요?\nA : 관리자의 DM으로 계약 철회관련 메시지를 보내시면 됩니다. 단, 이때는 사용자가 계약조건을 단 한번도 위반하지 않았을때 계약철회가 가능합니다.")
        await channel.send(embed=embed)

        f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
        f.write(log + "\n["+now_time+"] ID "+str(id)+" : 사용권 계약 1 조회")
        f.close()

    if message.content == "이루다 내돈":
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
            my_money = f.read()
            f.close()

            await channel.send("제가 조회해본 결과, <@"+str(id)+">님의 잔돈은\n총 `"+str(my_money)+"`원 이예요.")

        else:
            await channel.send("음... 당신은 아직 통장을 만들지 않았어요. '이루다 통장생성' 명령어를 통해 통장을 먼저 생성해주세요!\n앗, 그 전에 '이루다 사용권계약 1'명령어로 사용권 계약을 확인하는 것도 잊지 말아요!")
        
    if message.content == "이루다 기본배팅":
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
            my_money = f.read()
            f.close()

            if int(my_money) > 0:
                await channel.send("배팅이 시작되었어요! 랜덤변수에서 나온 숫자를 통해 `X0`, `X2`, `X4`를 정해요.")

                rand = random.uniform(0,10)
                rand = int(rand)

                if rand < 1:
                    await channel.send("<@"+str(id)+">님,\n이런! 당신의 배팅 결과는 `X0`이예요... 당신의 모든 돈을 잃어버렸어요... 너무 실망하지 말아요... \n'이루다 돈받기' 명령어를 이용해 무료요금 `10`원을 되돌려받아요.")

                    f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                    f.write('0')
                    f.close()

                if rand > 0 and rand < 7:
                    serv = random.uniform(10,1000)
                    serv = int(serv)

                    await channel.send("<@"+str(id)+">님,\n당신의 배팅 결과는 `X2`이예요! 양호한 결과군요!\n이용감사서비스 `"+str(serv)+"`원도 추가 적립해드릴게요!")

                    tot_money = (int(my_money) * 2) + int(serv)
                    f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                    f.write(str(tot_money))
                    f.close()
                    await channel.send("방금 통장에 잔액이 `"+str(tot_money)+"`원이 되었어요! 축하드려요!")

                if rand > 6:
                    serv = random.uniform(2000,10000)
                    serv = int(serv)

                    await channel.send("<@"+str(id)+">님,\n와우! 당신의 배팅 결과는 `X4`이군요! 엄청난 결과예요!\n이용감사서비스 `"+str(serv)+"`원도 추가 적립해드릴게요!")

                    tot_money = (int(my_money) * 4) + int(serv)
                    f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                    f.write(str(tot_money))
                    f.close()
                    await channel.send("방금 통장에 잔액이 `"+str(tot_money)+"`원이 되었어요! 축하드려요!")
            else:
                await channel.send("이런! 당신은 돈이 없군요... '이루다 돈받기' 명령어로 `10`원을 무료적립 해주세요.")

        else:
            await channel.send("음... 당신은 아직 통장을 만들지 않았어요. '이루다 통장생성' 명령어를 통해 통장을 먼저 생성해주세요!\n앗, 그 전에 '이루다 사용권계약 1'명령어로 사용권 계약을 확인하는 것도 잊지 말아요!")

    if message.content == "이루다 돈받기":
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
            my_money = f.read()
            f.close()

            if int(my_money) == 0:
                await channel.send("이런.. 모든 돈을 잃으셨군요. 이곳에 찾아오셨으니 `10`원을 무료 적립 해드릴께요.")
                f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                f.write('10')
                f.close()
            else:
                await channel.send("세상에나! 당신은 통장에 `"+my_money+"`원이나 가지고 계셨군요!\n하지만 이곳은 안타깝게도 돈을 모두 소진한 사람에게만 돈을 나누어 주는 곳이예요.")
        else:
            await channel.send("음... 당신은 아직 통장을 만들지 않았어요. '이루다 통장생성' 명령어를 통해 통장을 먼저 생성해주세요!\n앗, 그 전에 '이루다 사용권계약 1'명령어로 사용권 계약을 확인하는 것도 잊지 말아요!")

    if message.content == "이루다 스릴배팅":
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
            my_money = f.read()
            f.close()

            if int(my_money) > 0:
                await channel.send("배팅이 시작되었어요! 랜덤변수에서 나온 숫자를 통해 `X0`, `X10`을 정해요.")

                rand = random.uniform(0,10)
                rand = int(rand)

                if rand < 9:
                    await channel.send("<@"+str(id)+">님,\n이런! 당신의 배팅 결과는 `X0`이예요... 당신의 모든 돈을 잃어버렸어요... 너무 실망하지 말아요... \n'이루다 돈받기' 명령어를 이용해 무료요금 `10`원을 되돌려받아요.")

                    f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                    f.write('0')
                    f.close()

                if rand > 8:
                    serv = random.uniform(10000,20000)
                    serv = int(serv)

                    await channel.send("<@"+str(id)+">님,\n결국엔 해내셨군요! 당신의 배팅 결과는 `X10`이예요! 엄청난 결과군요!\n이용감사서비스 `"+str(serv)+"`원도 추가 적립해드릴게요!")

                    tot_money = (int(my_money) * 2) + int(serv)
                    f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                    f.write(str(tot_money))
                    f.close()
                    await channel.send("방금 통장에 잔액 `"+str(tot_money)+"`원이 되었어요! 축하드려요!")
            else:
                await channel.send("이런! 당신은 돈이 없군요... '이루다 돈받기' 명령어로 `10`원을 무료적립 해주세요.")

        else:
            await channel.send("음... 당신은 아직 통장을 만들지 않았어요. '이루다 통장생성' 명령어를 통해 통장을 먼저 생성해주세요!\n앗, 그 전에 '이루다 사용권계약 1'명령어로 사용권 계약을 확인하는 것도 잊지 말아요!")

    if message.content.startswith("이루다 돈선물"):
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
            my_money = f.read()
            f.close()

            if message.content[8:].startswith("<@"):
                target = re.findall(r'\d+', message.content)
                target = target[0]
                target = str(target)

                if message.content[31:] != "" and not(" " in message.content[31:]):
                    
                    if os.path.isfile("C:/iruda/money/"+target+".txt"):
                        
                        if int(my_money) >= int(message.content[31:]) and 0 < int(message.content[31:]):
                            f = open("C:/iruda/money/"+target+".txt", 'r')
                            gift_money = f.read()
                            f.close()

                            f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                            my_money = str(int(my_money) - int(message.content[31:]))
                            f.write(my_money)
                            f.close()

                            f = open("C:/iruda/money/"+target+".txt", 'w')
                            gift_money = str(int(gift_money) + int(message.content[31:]))
                            f.write(gift_money)
                            f.close()

                            await channel.send("<@"+str(id)+">님이 <@"+target+">님에게 총 `"+message.content[31:]+"`원을 선물해 주셨어요.\n따라서 <@"+str(id)+">님의 잔액은 `"+my_money+"`원, <@"+target+">님의 잔액은 `"+gift_money+"`원입니다.")                       
                        else:
                            await channel.send("선물할 금액이 보유한 잔고를 초과하거나, 보낼 돈이 음수예요.")
                    else:
                        await channel.send("선물할 사람의 통장이 존재하지 않아요.")
                else:
                    await channel.send("보낼 돈에 띄어쓰기가 포함되었거나, 보낼 돈이 정의되지 않았어요. 메시지를 다시한번 확인해주세요!")
            else:
                await channel.send("보낼 사람이 언급되지 않았어요. 메시지를 다시한번 확인해주세요!")
        else:
            await channel.send("음... 당신은 아직 통장을 만들지 않았어요. '이루다 통장생성' 명령어를 통해 통장을 먼저 생성해주세요!\n앗, 그 전에 '이루다 사용권계약 1'명령어로 사용권 계약을 확인하는 것도 잊지 말아요!")

    if message.content == "이루다 미친배팅":
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
            my_money = f.read()
            f.close()

            if int(my_money) > 100000:
                await channel.send("배팅이 시작되었어요! 랜덤변수에서 나온 숫자를 통해 `X0`, `X100000`을 정해요.")

                rand = random.uniform(0,100)
                rand = int(rand)

                if rand < 95:
                    await channel.send("<@"+str(id)+">님,\n이런! 당신의 배팅 결과는 `X0`이예요... 당신의 모든 돈을 잃어버렸어요... 너무 실망하지 말아요... \n'이루다 돈받기' 명령어를 이용해 무료요금 `10`원을 되돌려받아요.")

                    f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                    f.write('0')
                    f.close()

                if rand > 94:
                    serv = random.uniform(99999999,299999999)
                    serv = int(serv)

                    await channel.send("<@"+str(id)+">님,\n당신은 사람이 아니군요! 당신의 배팅 결과는 `X100000`이예요! 엄청난 결과군요!\n이용감사서비스 `"+str(serv)+"`원도 추가 적립해드릴게요!")

                    tot_money = (int(my_money) * 2) + int(serv)
                    f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                    f.write(str(tot_money))
                    f.close()
                    await channel.send("방금 통장에 잔액이 `"+str(tot_money)+"`원이 되었어요! 축하드려요!")
            else:
                await channel.send("이런! 죄송하지만, 미친배팅 기능은 자산이 `100000`원 이상일때만 이용할 수 있어요...ㅜ")

        else:
            await channel.send("음... 당신은 아직 통장을 만들지 않았어요. '이루다 통장생성' 명령어를 통해 통장을 먼저 생성해주세요!\n앗, 그 전에 '이루다 사용권계약 1'명령어로 사용권 계약을 확인하는 것도 잊지 말아요!")

    if message.content.startswith("이루다 조건배팅"):
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
            my_money = f.read()
            f.close()

            if not(message.content[9:] == "") and int(my_money) > 0 and int(message.content[9:]) <= int(my_money) and not(" " in message.content[9:]):
                await channel.send(message.content[9:]+"원을 배팅 시작할게요. 각각 `50%`의 확률로 실패 / 성공이 결정되요!")

                rand = random.uniform(0,2)
                rand = int(rand)

                if rand == 0:
                    await channel.send("<@"+str(id)+">님,\n이런! 당신의 배팅에 실패했어요... 당신은 당신이 건 돈인 `"+message.content[9:]+"`원을 잃었어요.\n이제 당신의 잔고는 `"+str(int(my_money)-int(message.content[9:]))+"`원이예요.\n만약 돈이 없다면, '이루다 돈받기' 명령어를 이용해 무료요금 `10`원을 되돌려받아요.")

                    f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                    f.write(str(int(my_money)-int(message.content[9:])))
                    f.close()

                if rand > 0:
                    rx1 = random.uniform(2,4)
                    rx1 = int(rx1)

                    if rx1 == 2:
                        await channel.send("우와! <@"+str(id)+">님은 조건 배팅에 성공하셔서 당신이 건 돈의 `X1.2`를 수령하게 되었어요!\n당신은 `"+message.content[9:]+"`원을 걸어서, 총 `"+str(int(int(message.content[9:]) * 1.2))+"`원을 수령해요.\n*조건배팅 이용시, 추가 보너스 수령액은 존재하지 않아요.")

                        tot_money = int(my_money) - int(message.content[9:]) + (int(int(message.content[9:]) * 1.2))
                        f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                        f.write(str(tot_money))
                        f.close()
                    
                        await channel.send("방금 통장에 잔액이 "+str(tot_money)+"원이 되었어요! 축하드려요!")

                    if rx1 == 3:
                        await channel.send("우와! <@"+str(id)+">님은 조건 배팅에 성공하셔서 당신이 건 돈의 `X1.3`을 수령하게 되었어요!\n당신은 `"+message.content[9:]+"`원을 걸어서, 총 `"+str(int(int(message.content[9:]) * 1.3))+"`원을 수령해요.\n*조건배팅 이용시, 추가 보너스 수령액은 존재하지 않아요.")

                        tot_money = int(my_money) - int(message.content[9:]) + (int(int(message.content[9:]) * 1.3))
                        f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                        f.write(str(tot_money))
                        f.close()

                        await channel.send("방금 통장에 잔액이 "+str(tot_money)+"원이 되었어요! 축하드려요!")

                    if rx1 == 4:
                        await channel.send("우와! <@"+str(id)+">님은 조건 배팅에 성공하셔서 당신이 건 돈의 `X1.4`를 수령하게 되었어요!\n당신은 `"+message.content[9:]+"`원을 걸어서, 총 `"+str(int(int(message.content[9:]) * 1.4))+"`원을 수령해요.\n*조건배팅 이용시, 추가 보너스 수령액은 존재하지 않아요.")

                        tot_money = int(my_money) - int(message.content[9:]) + (int(int(message.content[9:]) * 1.4))
                        f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                        f.write(str(tot_money))
                        f.close()
                    
                        await channel.send("방금 통장에 잔액이 "+str(tot_money)+"원이 되었어요! 축하드려요!")
            else:
                await channel.send("이런! 문제가 발생했어요. 조건배팅에 걸 돈이 정의되지 않았거나, 또는 조건배팅에 건 돈이 잔고를 초과하거나, 조건배팅에 건 돈에 띄어쓰기가 포함되요. 잔고를 다시한번 확인하거나, 자신의 메시지를 다시한번 확인한 후 조건배팅을 시작해주세요!")

        else:
            await channel.send("음... 당신은 아직 통장을 만들지 않았어요. '이루다 통장생성' 명령어를 통해 통장을 먼저 생성해주세요!\n앗, 그 전에 '이루다 사용권계약 1'명령어로 사용권 계약을 확인하는 것도 잊지 말아요!")

# 스톤 관련 명령어
    if message.content == "이루다 스톤":
        rspd = rspd + 1
        f = open("C:/iruda/stone/stone.txt", 'r')
        stone = f.read()
        f.close()

        await channel.send("현재 충전되어있는 S+ONE은 `"+stone+"`개 예요.")

    if message.content == "이루다 모래시계":
        rspd =  rspd + 1
        if auth == 'ad':
            f = open("c:/iruda/stone/trail.txt", 'r')
            hourglass_1 = f.read()
            f.close()

            f = open("c:/iruda/stone/normal.txt", 'r')
            hourglass_2 = f.read()
            f.close()

            f = open("c:/iruda/stone/gold.txt", 'r')
            hourglass_3 = f.read()
            f.close()

            f = open("c:/iruda/stone/ultimate.txt", 'r')
            hourglass_4 = f.read()
            f.close()

            f = open("c:/iruda/stone/plenium.txt", 'r')
            hourglass_5 = f.read()
            f.close()

            f = open("c:/iruda/stone/admiral.txt", 'r')
            hourglass_6 = f.read()
            f.close()

            await channel.send("현재 보유하고 있는 모래시계 현황이예요.\n[모래시계 보유 현황]\n 트레일 모래시계 : `"+hourglass_1+"`개\n 일반 모래시계 : `"+hourglass_2+"개`\n 골드 모래시계 : `"+hourglass_3+"`개\n 얼티밋 모래시계 : `"+hourglass_4+"`개\n 플레니엄 모래시계 : `"+hourglass_5+"`개\n 어드미럴 모래시계 : `"+hourglass_6+"`개\n\n[TIP] 현재 보유하고 있는 S+ONE정보를 보시려면 '이루다 스톤'을 입력해주세요!")


    if message.content == "이루다 스톤구매":
        rspd = rspd + 1
        await channel.send("[스톤 종류별 가격]\nS+ONE `3`개 - `100`원\n S+ONE `18(15+3)`개 - ~~`500`원~~ 할인가: `200`원\n S+ONE `49(45+4)`개 - ~~`1500`원~~ 할인가: `1300`원\n S+ONE `160(150+10)`개 - ~~`5000`원~~ 할인가: `4900`원\n\n구매의향이 있는경우 개발자에게 문의해주세요.\n환불정책에 관해서는 개발자에게 문의해주세요.")
        

    if message.content == "이루다 모래시계구매":
        rspd = rspd + 1
        f = open("C:/iruda/stone/stone.txt", 'r')
        stone = f.read()
        f.close()

        await channel.send("[모래시계 종류별 가격]\n 트레일 모래시계(15분) - `4`S+ONE\n 일반 모래시계(1시간) - `10`S+ONE\n 골드 모래시계(1개 무제한) - `99`S+ONE\n 얼티밋 모래시계(1일 무제한) - `139`S+ONE\n 플레니엄 모래시계(7일 무제한) - `415`S+ONE\n 어드미럴 모래시계(30일 무제한) - `1500`S+ONE\n\n현재, 충전되어있는 S+ONE은 `"+stone+"개`이에요.\n\n**모래시계 구매를 확정하시려면 '이루다 모래시계구매 (모래시계 번호)' 명령어를 입력하세요!**\n**[주의] 모래시계는 한번 구입하면 현금/S+ONE으로 환불이 불가합니다. 신중히 선택해주세요.**\n*모래시계 번호는 위에서부터 1번입니다.")

    if message.content == "이루다 모래시계구매 1":
        rspd = rspd + 1
        f = open("C:/iruda/stone/stone.txt", 'r')
        stone = f.read()
        f.close()
        if int(stone) >= 4:
            f = open("C:/iruda/stone/stone.txt", 'w')
            f.write(str(int(stone)-4))
            f.close()

            f = open("c:/iruda/stone/trail.txt", 'r')
            hourglass = f.read()
            f.close()

            f = open("c:/iruda/stone/trail.txt", 'w')
            f.write(str(int(hourglass)+1))
            f.close()

            await channel.send("`2`S+ONE을 사용해서 트레일 모래시계 `1`개를 구매했어요! 현재 보유하고 있는 S+ONE은 `"+str(int(stone)-4)+"`개, 보유하고 있는 트레일 모래시계는 `"+str(int(hourglass)+1)+"`개예요.")
        else:
            await channel.send("트레일 모래시계의 가격은 `4`S+ONE이예요. 하지만 현재 보유하고 있는 S+ONE은 `"+stone+"`개 뿐이예요...ㅜ")

    if message.content == "이루다 모래시계구매 2":
        rspd = rspd + 1
        f = open("C:/iruda/stone/stone.txt", 'r')
        stone = f.read()
        f.close()
        if int(stone) >= 10:
            f = open("C:/iruda/stone/stone.txt", 'w')
            f.write(str(int(stone)-10))
            f.close()

            f = open("c:/iruda/stone/normal.txt", 'r')
            hourglass = f.read()
            f.close()

            f = open("c:/iruda/stone/normal.txt", 'w')
            f.write(str(int(hourglass)+1))
            f.close()

            await channel.send("`10`S+ONE을 사용해서 일반 모래시계 `1`개를 구매했어요! 현재 보유하고 있는 S+ONE은 `"+str(int(stone)-10)+"`개, 보유하고 있는 일반 모래시계는 `"+str(int(hourglass)+1)+"`개예요.")
        else:
            await channel.send("일반 모래시계의 가격은 `10`S+ONE이예요. 하지만 현재 보유하고 있는 S+ONE은 `"+stone+"`개 뿐이예요...ㅜ")

    if message.content == "이루다 모래시계구매 3":
        rspd = rspd + 1
        f = open("C:/iruda/stone/stone.txt", 'r')
        stone = f.read()
        f.close()
        if int(stone) >= 99:
            f = open("C:/iruda/stone/stone.txt", 'w')
            f.write(str(int(stone)-99))
            f.close()

            f = open("c:/iruda/stone/gold.txt", 'r')
            hourglass = f.read()
            f.close()

            f = open("c:/iruda/stone/gold.txt", 'w')
            f.write(str(int(hourglass)+1))
            f.close()

            await channel.send("`99`S+ONE을 사용해서 골드 모래시계 `1`개를 구매했어요! 현재 보유하고 있는 S+ONE은 `"+str(int(stone)-99)+"`개, 보유하고 있는 골드 모래시계는 `"+str(int(hourglass)+1)+"`개예요.")
        else:
            await channel.send("골드 모래시계의 가격은 `99`S+ONE이예요. 하지만 현재 보유하고 있는 S+ONE은 `"+stone+"`개 뿐이예요...ㅜ")

    if message.content == "이루다 모래시계구매 4":
        rspd = rspd + 1
        f = open("C:/iruda/stone/stone.txt", 'r')
        stone = f.read()
        f.close()
        if int(stone) >= 139:
            f = open("C:/iruda/stone/stone.txt", 'w')
            f.write(str(int(stone)-139))
            f.close()

            f = open("c:/iruda/stone/ultimate.txt", 'r')
            hourglass = f.read()
            f.close()

            f = open("c:/iruda/stone/ultimate.txt", 'w')
            f.write(str(int(hourglass)+1))
            f.close()

            await channel.send("`139`S+ONE을 사용해서 얼티밋 모래시계 `1`개를 구매했어요! 현재 보유하고 있는 S+ONE은 `"+str(int(stone)-139)+"`개, 보유하고 있는 얼티밋 모래시계는 `"+str(int(hourglass)+1)+"`개예요.")
        else:
            await channel.send("얼티밋 모래시계의 가격은 `139`S+ONE이예요. 하지만 현재 보유하고 있는 S+ONE은 `"+stone+"`개 뿐이예요...ㅜ")

    if message.content == "이루다 모래시계구매 5":
        rspd = rspd + 1
        f = open("C:/iruda/stone/stone.txt", 'r')
        stone = f.read()
        f.close()
        if int(stone) >= 415:
            f = open("C:/iruda/stone/stone.txt", 'w')
            f.write(str(int(stone)-415))
            f.close()

            f = open("c:/iruda/stone/plenium.txt", 'r')
            hourglass = f.read()
            f.close()

            f = open("c:/iruda/stone/plenium.txt", 'w')
            f.write(str(int(hourglass)+1))
            f.close()

            await channel.send("`245`S+ONE을 사용해서 플레니엄 모래시계 `1`개를 구매했어요! 현재 보유하고 있는 S+ONE은 `"+str(int(stone)-415)+"`개, 보유하고 있는 플레니엄 모래시계는 `"+str(int(hourglass)+1)+"`개예요.")
        else:
            await channel.send("플레니엄 모래시계의 가격은 `415`S+ONE이예요. 하지만 현재 보유하고 있는 S+ONE은 `"+stone+"`개 뿐이예요...ㅜ")

    if message.content == "이루다 모래시계구매 6":
        rspd = rspd + 1
        f = open("C:/iruda/stone/stone.txt", 'r')
        stone = f.read()
        f.close()
        if int(stone) >= 1500:
            f = open("C:/iruda/stone/stone.txt", 'w')
            f.write(str(int(stone)-1500))
            f.close()

            f = open("c:/iruda/stone/admiral.txt", 'r')
            hourglass = f.read()
            f.close()

            f = open("c:/iruda/stone/admiral.txt", 'w')
            f.write(str(int(hourglass)+1))
            f.close()

            await channel.send("`1500`S+ONE을 사용해서 어드미럴 모래시계 `1`개를 구매했어요! 현재 보유하고 있는 S+ONE은 `"+str(int(stone)-1500)+"`개, 보유하고 있는 어드미럴 모래시계는 `"+str(int(hourglass)+1)+"`개예요.")
        else:
            await channel.send("어드미럴 모래시계의 가격은 `179스톤`이예요. 하지만 현재 보유하고 있는 S+ONE은 `"+stone+"`개 뿐이예요...ㅜ")

    
    if message.content.startswith("이루다 스톤코드 ") and rspd == 0:
        rspd = rspd + 1
        rccoupon = message.content[9:]
        if not(" " in rccoupon):
            if os.path.isfile("C:/iruda/stonecode/"+rccoupon+".txt"):
                f = open("C:/iruda/stonecode/"+rccoupon+".txt", 'r')
                coupon = f.read()
                f.close()

                coupon = coupon.split(".")
                reward = coupon[1]
                if int(coupon[0]) > 0:
                    if not(str(id) in coupon[2]):
                        f = open("C:/iruda/stone/stone.txt", 'r')
                        stone = f.read()
                        f.close()

                        f = open("C:/iruda/stone/stone.txt", 'w')
                        f.write(str(int(stone)+int(reward)))
                        f.close()

                        f = open("C:/iruda/stonecode/"+rccoupon+".txt", 'w')
                        f.write(str(int(coupon[0])-1)+"."+coupon[1]+"."+coupon[2]+"/"+str(id))
                        f.close()

                        await channel.send("<@"+str(id)+">님, S+ONE 코드 [`"+rccoupon+"`](을)를 사용해서 `"+reward+"`S+ONE이 수령되었어요.\n현재 보유하고 있는 S+ONE은 `"+str(int(stone)+int(reward))+"`개예요!")
                    else:
                        await channel.send("<@"+str(id)+">님은 이미 이 스S+ONE 코드를 사용했어요.\n스톤쿠폰은 한 명당 한 번만 사용할 수 있어요!")
                else:
                    await channel.send("이미 사용할 수 있는 모든 사람이 사용한 S+ONE 코드예요.\n다음 S+ONE 코드를 기다려주세요!")
            else:
                await channel.send("해당 쿠폰은 존재하지 않는 S+ONE 코드에요.")
        else:
            await channel.send("S+ONE 코드에 띄어쓰기가 포함되어 있어요. 메시지를 다시한번 확인해주세요!")

    if message.content == "이루다 모래시계사용 1":
        rspd = rspd + 1
        f = open("C:/iruda/stone/trail.txt", 'r')
        hourglass = f.read()
        f.close()
        if int(hourglass) >= 1:
            f = open("c:/iruda/stone/trail.txt", 'w')
            f.write(str(int(hourglass)-1))
            f.close()

            await channel.send("트레일 모래시계 `1`개를 사용했어요! 이제 남은 트레일 모래시계는 `"+str(int(hourglass)-1)+"`개예요.\n[TIP] 전체 모래시계 보유현황을 보려면, '이루다 모래시계'를 입력해주세요!")
        else:
            await channel.send("현재 보유하고 있는 트레일 모래시계가 없어요... S+ONE으로 구매해보는건 어떨까요? '이루다 모래시계구매'를 입력해봐요!")

    if message.content == "이루다 모래시계사용 2":
        rspd = rspd + 1
        f = open("C:/iruda/stone/normal.txt", 'r')
        hourglass = f.read()
        f.close()
        if int(hourglass) >= 1:
            f = open("c:/iruda/stone/normal.txt", 'w')
            f.write(str(int(hourglass)-1))
            f.close()

            await channel.send("일반 모래시계 `1`개를 사용했어요! 이제 남은 일반 모래시계는 `"+str(int(hourglass)-1)+"`개예요.\n[TIP] 전체 모래시계 보유현황을 보려면, '이루다 모래시계'를 입력해주세요!")
        else:
            await channel.send("현재 보유하고 있는 일반 모래시계가 없어요... S+ONE으로 구매해보는건 어떨까요? '이루다 모래시계구매'를 입력해봐요!")

    if message.content == "이루다 모래시계사용 3":
        rspd = rspd + 1
        f = open("C:/iruda/stone/gold.txt", 'r')
        hourglass = f.read()
        f.close()
        if int(hourglass) >= 1:
            f = open("c:/iruda/stone/gold.txt", 'w')
            f.write(str(int(hourglass)-1))
            f.close()

            await channel.send("골드 모래시계 `1`개를 사용했어요! 이제 남은 골드 모래시계는 `"+str(int(hourglass)-1)+"`개예요.\n[TIP] 전체 모래시계 보유현황을 보려면, '이루다 모래시계'를 입력해주세요!")
        else:
            await channel.send("현재 보유하고 있는 골드 모래시계가 없어요... S+ONE으로 구매해보는건 어떨까요? '이루다 모래시계구매'를 입력해봐요!")

    if message.content == "이루다 모래시계사용 4":
        rspd = rspd + 1
        f = open("C:/iruda/stone/ultimate.txt", 'r')
        hourglass = f.read()
        f.close()
        if int(hourglass) >= 1:
            f = open("c:/iruda/stone/ultimate.txt", 'w')
            f.write(str(int(hourglass)-1))
            f.close()

            await channel.send("얼티밋 모래시계 `1개`를 사용했어요! 이제 남은 얼티밋 모래시계는 `"+str(int(hourglass)-1)+"개`예요.\n[TIP] 전체 모래시계 보유현황을 보려면, '이루다 모래시계'를 입력해주세요!")
        else:
            await channel.send("현재 보유하고 있는 얼티밋 모래시계가 없어요... S+ONE으로 구매해보는건 어떨까요? '이루다 모래시계구매'를 입력해봐요!")

    if message.content == "이루다 모래시계사용 5":
        rspd = rspd + 1
        f = open("C:/iruda/stone/plenium.txt", 'r')
        hourglass = f.read()
        f.close()
        if int(hourglass) >= 1:
            f = open("c:/iruda/stone/plenium.txt", 'w')
            f.write(str(int(hourglass)-1))
            f.close()

            await channel.send("플레니엄 모래시계 `1`개를 사용했어요! 이제 남은 플레니엄 모래시계는 `"+str(int(hourglass)-1)+"`개예요.\n[TIP] 전체 모래시계 보유현황을 보려면, '이루다 모래시계'를 입력해주세요!")
        else:
            await channel.send("현재 보유하고 있는 플레니엄 모래시계가 없어요... S+ONE으로 구매해보는건 어떨까요? '이루다 모래시계구매'를 입력해봐요!")

    if message.content == "이루다 모래시계사용 6":
        rspd = rspd + 1
        f = open("C:/iruda/stone/admiral.txt", 'r')
        hourglass = f.read()
        f.close()
        if int(hourglass) >= 1:
            f = open("c:/iruda/stone/admiral.txt", 'w')
            f.write(str(int(hourglass)-1))
            f.close()

            await channel.send("어드미럴 모래시계 `1`개를 사용했어요! 이제 남은 어드미럴 모래시계는 `"+str(int(hourglass)-1)+"`개예요.\n[TIP] 전체 모래시계 보유현황을 보려면, '이루다 모래시계'를 입력해주세요!")
        else:
            await channel.send("현재 보유하고 있는 어드미럴 모래시계가 없어요... S+ONE으로 구매해보는건 어떨까요? '이루다 모래시계구매'를 입력해봐요!")

    if message.content.startswith("이루다 스톤충전 "):
        rspd = rspd + 1

        msgsplit = message.content.split(" ")
        count = msgsplit[2]
        identity_verification = msgsplit[3]
        
        f = open("C:/iruda/.security/identity_verification.txt", 'r')
        identity_verification_check = f.read()
        f.close()

        if auth == "ad":
            if not(identity_verification_check == "null"):
                if identity_verification == identity_verification_check:
                    f = open("C:/iruda/stone/stone.txt", 'r')
                    stone = f.read()
                    f.close()

                    f = open("C:/iruda/stone/stone.txt", 'w')
                    f.write(str(int(stone)+int(count)))
                    f.close()

                    f = open("C:/iruda/.security/identity_verification.txt", 'w')
                    f.write("null")
                    f.close()

                    await channel.send("관리자님, S+ONE `"+count+"`개를 충전해서 총 S+ONE이 `"+str(int(stone)+int(count))+"`개가 되었어요.")
                else:
                    await channel.send("본인인증코드가 일치하지 않아요.")
            else:
                await channel.send("본인인증코드가 더이상 유효하지 않아요. 본인인증코드를 새로 발급해주세요.")
        else:
            user = app.get_user(500251192883150859)
            await user.send("[중요] 관리자님, <@"+str(id)+">님이 본인인증코드인증을 시도하셨습니다.")
            await channel.send("정상적으로 신고처리되었습니다.")
            
    if message.content.startswith("이루다 스톤사용 "):
        rspd = rspd + 1

        msgsplit = message.content.split(" ")
        count = msgsplit[2]
        identity_verification = msgsplit[3]
        
        f = open("C:/iruda/.security/identity_verification.txt", 'r')
        identity_verification_check = f.read()
        f.close()

        if auth == "ad":
            if not(identity_verification_check == "null"):
                if identity_verification == identity_verification_check:
                    f = open("C:/iruda/stone/stone.txt", 'r')
                    stone = f.read()
                    f.close()

                    f = open("C:/iruda/stone/stone.txt", 'w')
                    f.write(str(int(stone)-int(count)))
                    f.close()
                    
                    f = open("C:/iruda/.security/identity_verification.txt", 'w')
                    f.write("null")
                    f.close()

                    await channel.send("관리자님, S+ONE `"+count+"`개를 사용해서 총 S+ONE이 `"+str(int(stone)-int(count))+"`개가 남았어요.")
                else:
                    await channel.send("본인인증코드가 일치하지 않아요.")
            else:
                await channel.send("본인인증코드가 더이상 유효하지 않아요. 본인인증코드를 새로 발급해주세요.")
        else:
            user = app.get_user(500251192883150859)
            await user.send("[중요] 관리자님, <@"+str(id)+">님이 본인인증코드인증을 시도하셨습니다.")
            await channel.send("정상적으로 신고처리되었습니다.")

#보안
    if message.content == "이루다 본인인증코드발급":
        rspd = rspd + 1
        if auth == 'ad':
            identity_verification_code = random.uniform(10000000000000,99999999999999)
            identity_verification_code = str(int(identity_verification_code))
            f = open("C:/iruda/.security/identity_verification.txt", 'w')
            f.write(identity_verification_code)
            f.close()

            user = app.get_user(500251192883150859)
            await user.send("[이루다 본인확인 서비스]\n요청된 본인인증 코드는 ["+identity_verification_code+"] 이예요.\n\n`요청 ID : "+str(id)+"`")
            if id != 500251192883150859:
                await channel.send("[이루다 본인확인서비스]\n개발자님의 DM에 본인인증 코드를 전송해놨어요.")
        else:
            user = app.get_user(500251192883150859)
            await user.send("[중요] 관리자님, <@"+str(id)+">님이 본인인증코드발급을 시도하셨습니다.")
            await channel.send("정상적으로 신고처리되었습니다.")

    if message.content == "이루다 본인인증코드해제":
        rspd = rspd + 1
        if auth == 'ad':
            f = open("C:/iruda/.security/identity_verification.txt", 'w')
            f.write("null")
            f.close()

            user = app.get_user(500251192883150859)
            await user.send("[이루다 본인확인 서비스]\n요청된 본인인증코드가 해제되었어요.\n\n`요청 ID : "+str(id)+"`")
            if id != 500251192883150859:
                await channel.send("[이루다 본인확인서비스]\n본인인증코드가 해제되었어요.")
        else:
            user = app.get_user(500251192883150859)
            await user.send("[중요] 관리자님, <@"+str(id)+">님이 본인인증코드해제을 시도하셨습니다.")
            await channel.send("정상적으로 신고처리되었습니다.")


# 쿠폰코드
    if message.content.startswith("이루다 쿠폰입력"):
        rspd = rspd + 1
        rccoupon = message.content[9:]
        if not(" " in rccoupon):
            if os.path.isfile("C:/iruda/coupon/"+rccoupon+".txt"):
                f = open("C:/iruda/coupon/"+rccoupon+".txt", 'r')
                coupon = f.read()
                f.close()

                coupon = coupon.split(".")
                reward = coupon[1]
                if int(coupon[0]) > 0:
                    if not(str(id) in coupon[2]):
                        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
                            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
                            my_money = f.read()
                            f.close()

                            f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                            f.write(str(int(my_money)+int(reward)))
                            f.close()

                            f = open("C:/iruda/coupon/"+rccoupon+".txt", 'w')
                            f.write(str(int(coupon[0])-1)+"."+coupon[1]+"."+coupon[2]+"/"+str(id))
                            f.close()

                            await channel.send("<@"+str(id)+">님, 쿠폰코드 [`"+rccoupon+"`](이)가 일치하여 방금 통장에 `"+reward+"`원이 추가되었어요.")

                            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                            f.write(log + "\n["+now_time+"] ID "+str(id)+" : ["+rccoupon+"](을)를 쿠폰코드로 사용")
                            f.close()
                        else:
                            await channel.send("음... 당신은 아직 통장을 만들지 않았어요. '이루다 통장생성' 명령어를 통해 통장을 먼저 생성해주세요!\n앗, 그 전에 '이루다 사용권계약 1'명령어로 사용권 계약을 확인하는 것도 잊지 말아요!")
                    else:
                        await channel.send("<@"+str(id)+">님은 이미 이 쿠폰을 사용했어요.\n쿠폰은 한 명당 한 번만 사용할 수 있어요!")
                else:
                    await channel.send("이미 사용할 수 있는 모든 사람이 사용한 쿠폰이예요.\n다음 쿠폰을 기다려주세요!")
            else:
                await channel.send("해당 쿠폰은 존재하지 않는 쿠폰이에요.")
        else:
            await channel.send("쿠폰코드에 띄어쓰기가 포함되어 있어요. 메시지를 다시한번 확인해주세요!")

#코스피 명령어
    if message.content == "이루다 코스피지수":
        rspd = rspd + 1
        await channel.send("웹 사이트 `https://kr.investing.com/indices/kospi`에서 코스피지수를 불러오는 중이예요...")

        url = 'https://kr.investing.com/indices/kospi'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(res, 'html.parser')
        kospi = soup.find('span', class_="arial_26 inlineblock pid-37426-last").get_text()
        kospi = kospi.replace(",","")

        await channel.send("현재 코스피 지수는 아래와 같아요.\n`"+kospi+"`")

    if message.content == "이루다 코스피":
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/stock/"+str(id)+".txt"):
            await channel.send("이루다 봇의 코스피 시스템은 실제 코스피 지수를 기반으로 하여 구축된 서비스예요.\n실제 코스피 주식을 매수하는 것은 아니지만, 실제 코스피 지수에 맞춰 이루다 가상화폐를 통해 주식을 매수하고, 코스피 지수가 올라가면 내 주식을 매도하여 돈을 불릴 수 있어요.\n\n예를 들어, 현제 코스피 지수가 `1900`이라면, 이루다 가상화폐 `1900`원으로 코스피 주식 `1`주를 살 수 있고, 나중에 코스피 지수가 오르면, 더 비싼 값으로 되팔 수 있어요.\n이루다 봇의 코스피 시스템 관련 명령어를 보고 싶다면, '이루다 도움말'을 사용해보세요!\n\n[코스피 매수하기]\n이루다 코스피 매수 (매수할 주식[개])\n[코스피 매도하기]\n이루다 코스피 매도 (매도할 주식[개])")
        else:
            await channel.send("<@"+str(id)+">님은 아직 주식통장이 없군요! '이루다 사용권계약 2'명령어로 주식 / 코스피 관련 사용권 계약을 확인해주세요!")

    if message.content == "이루다 사용권계약 2":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 코스피 시스템 최종 사용권 계약", description="이루다 봇 내에서 유통 / 판매되는 주식의 가치는 없습니다. 이루다 주식 명령어는 실제 주식을 매수하거나, 매도하는 것이 아니며 이루다 봇 내에서 유통되는 주식은 실제 코스피에 반영되지 않음을 알립니다.\n\n[FAQ]\nQ : 사용자 계약에 동의하지 않으려면 어떻게 하야 하나요?\nA : 이루다 주식 관련 명령어를 사용하지 않으면 됩니다.\n\nQ : 이미 이루다 주식 명령어를 사용했는데, 나중에 계약을 철회하고 싶다면 어떻게 해야 하나요?\nA : 관리자의 DM으로 계약 철회관련 메시지를 보내시면 됩니다. 단, 이때는 사용자가 계약조건을 단 한번도 위반하지 않았을때 계약철회가 가능합니다.")
        await channel.send(embed=embed)
        await channel.send("**사용권 계약에 동의**하고 **주식 명령어를 사용**하고 싶으시다면, '이루다 주식통장생성'명령어를 입력해주세요!")

    if message.content == "이루다 주식통장생성":
        rspd = rspd + 1
        if not(os.path.isfile("C:/iruda/stock/"+str(id)+".txt")):
            f = open("C:/iruda/stock/"+str(id)+".txt", 'w')
            f.write("0.0")
            f.close()

            await channel.send(":white_check_mark: <@"+str(id)+">님의 주식통장이 개설되었어요!\n현재 매수 / 매도되고 있는 코스피 지수를 확인하려면, '이루다 코스피지수'명령어를 입력해주세요.\n주식을 사거나 되팔고 싶으시다면 '이루다 코스피'에서 더 많은 정보를 확인해주세요!")
        else:
            await channel.send("<@"+str(id)+">님은 벌써 주식통장을 만들었어요! '이루다 내주식'명령어로 나의 주식정보를 확인해보세요!")

    if message.content == "이루다 내주식":
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/stock/"+str(id)+".txt") and os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            await channel.send("코스피지수를 불러올때까지 잠시만 기다려주세요...")

            url = 'https://kr.investing.com/indices/kospi'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(res, 'html.parser')
            kospi = soup.find('span', class_="arial_26 inlineblock pid-37426-last").get_text()
            kospi = kospi.replace(",","")
            kospi = round(float(kospi))
            kospi = str(kospi)

            f = open("C:/iruda/stock/"+str(id)+".txt", 'r')
            my_stock = f.read()
            f.close()
            my_stock = my_stock.split(".")

            if int(my_stock[1]) != 0:
                lst_purch = int(my_stock[1]) / int(my_stock[0])
                pre_purch = int(kospi)

                await channel.send("다음은 <@"+str(id)+">님의 주식 정보예요.\n```[나의 주식 정보]\n현재 코스피 지수 : "+kospi+"\n보유 주식 : "+my_stock[0]+"(개)\n투자한 돈 : "+my_stock[1]+"원\n현재 가치 : "+str(int(my_stock[0])*int(kospi))+"원\n주식 매도 시 이익(손해) : 주식 개 당 "+str(pre_purch-lst_purch)+"원```")
            else:
                await channel.send("아직 보유한 주식이 없어요. 주식을 매수한 후, 명령어를 사용해주세요!")
        else:
            await channel.send("아직 이루다 봇 주식 통장을 만들지 않았군요! '이루다 도움말'을 이용하여 가상계좌를 만들어주세요!")

    if message.content.startswith("이루다 코스피 매수"):
        rspd = rspd + 1
        if not(message.content[11:] == ""):
            await channel.send("코스피 지수를 불러오는 중이예요. 잠시만 기다려 주세요...\n(인터넷 환경에 따라 속도가 차이날 수 있습니다.)\n[TIP :bulb:] 모든 코스피 거래는 코스피 지수를 소수첫째자리에서 반올림 해 자연수로 계산해요.")

            url = 'https://kr.investing.com/indices/kospi'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(res, 'html.parser')
            kospi = soup.find('span', class_="arial_26 inlineblock pid-37426-last").get_text()
            kospi = kospi.replace(",","")
            kospi = round(float(kospi))
            kospi = str(kospi)

            if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
                f = open("C:/iruda/money/"+str(id)+".txt", 'r')
                my_money = f.read()
                f.close()

                if os.path.isfile("C:/iruda/stock/"+str(id)+".txt"):

                    if int(message.content[11:])*int(kospi) < int(my_money):
                        f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                        f.write(str(int(my_money)-(int(message.content[11:])*int(kospi))))
                        f.close()

                        f = open("C:/iruda/stock/"+str(id)+".txt", 'r')
                        my_stock = f.read()
                        f.close()
                        my_stock = my_stock.split(".")

                        f = open("C:/iruda/stock/"+str(id)+".txt", 'w')
                        f.write(str(int(my_stock[0])+int(message.content[11:]))+"."+str(int(my_stock[1])+(int(message.content[11:])*int(kospi))))
                        f.close()

                        await channel.send("<@"+str(id)+">님,\n코스피 지수 `"+kospi+"`에 따라서 요구하신 `"+message.content[11:]+"`주가 총 `"+str(int(message.content[11:])*int(kospi))+"`원에 거래되었어요.\n따라서 <@"+str(id)+">님의 가상계좌 잔액은 `"+str(int(my_money)-(int(message.content[11:])*int(kospi)))+"`원, 보유하고 있는 총 주식[개]는 `"+str(int(my_stock[0])+int(message.content[11:]))+"`개에요.")
                    else:
                        await channel.send("현재 요구하신 `"+message.content[11:]+"`주의 가격은 `"+str(int(message.content[11:])*int(kospi))+"`원으로, <@"+str(id)+">님의 통장잔고 `"+my_money+"`원을 초과해요.")
                else:
                    await channel.send("아직 주식통장을 만들지 않았네요! '이루다 사용권계약 2'명령어로 주식통장을 만들어주세요!")
            else:
                await channel.send("아직 이루다 봇 가상계좌를 만들지 않았네요! '이루다 도움말'을 이용하여 가상계좌를 만들어주세요!")

    if message.content.startswith("이루다 코스피 매도"):
        rspd = rspd + 1
        if not(message.content[11:] == ""):
            await channel.send("코스피 지수를 불러오는 중이예요. 잠시만 기다려 주세요...\n(인터넷 환경에 따라 속도가 차이날 수 있습니다.)\n[TIP :bulb:] '이루다 내주식'명령어로 나의 주식 정보를 불러올 수 있어요.")

            url = 'https://kr.investing.com/indices/kospi'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(res, 'html.parser')
            kospi = soup.find('span', class_="arial_26 inlineblock pid-37426-last").get_text()
            kospi = kospi.replace(",","")
            kospi = round(float(kospi))
            kospi = str(kospi)

            if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
                f = open("C:/iruda/money/"+str(id)+".txt", 'r')
                my_money = f.read()
                f.close()

                if os.path.isfile("C:/iruda/stock/"+str(id)+".txt"):
                    f = open("C:/iruda/stock/"+str(id)+".txt", 'r')
                    my_stock = f.read()
                    f.close()
                    my_stock = my_stock.split(".")

                    if int(message.content[11:]) <= int(my_stock[0]):
                        f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                        f.write(str(int(my_money)+(int(message.content[11:])*int(kospi))))
                        f.close()

                        if int(my_stock[0])-int(message.content[11:]) == 0:
                            f = open("C:/iruda/stock/"+str(id)+".txt", 'w')
                            f.write(str(int(my_stock[0])-int(message.content[11:]))+".0")
                            f.close()
                        else:
                            f = open("C:/iruda/stock/"+str(id)+".txt", 'w')
                            f.write(str(int(my_stock[0])-int(message.content[11:]))+"."+str(int(my_stock[1])-(int(message.content[11:])*int(kospi))))
                            f.close()

                        lst_purch = int(my_stock[1]) / int(my_stock[0])
                        pre_purch = int(kospi)

                        await channel.send("<@"+str(id)+">님,\n코스피 지수 `"+kospi+"`에 따라서 요구하신 `"+message.content[11:]+"`주가 총 `"+str(int(message.content[11:])*int(kospi))+"`원에 반환되었어요.\n따라서 <@"+str(id)+">님의 가상계좌 잔액은 `"+str(int(my_money)+(int(message.content[11:])*int(kospi)))+"`원, 보유하고 있는 총 주식[개]는 `"+str(int(my_stock[0])-int(message.content[11:]))+"`개에요.\n이번 매도로 인해 발생한 이익(손해)는 주식 개 당 `"+str(pre_purch-lst_purch)+"`원이고,\n총 수익(손해)는 `"+str(int(message.content[11:])*int(kospi)-int(my_stock[1]))+"`원이에요.")
                    else:
                        await channel.send("현재 요구하신 `"+message.content[11:]+"`주는 <@"+str(id)+">님의 보유 주식 `"+my_stock[0]+"`개를 초과해요.")
                else:
                    await channel.send("아직 주식통장을 만들지 않았네요! '이루다 사용권계약 2'명령어로 주식통장을 만들어주세요!")
            else:
                await channel.send("아직 이루다 봇 가상계좌를 만들지 않았네요! '이루다 도움말'을 이용하여 가상계좌를 만들어주세요!")

#가르치기 확인
    if (message.content.startswith("이루다")) and (os.path.isfile("C:/iruda/learn/"+message.content[4:]+".txt")) and (rspd == 0):
        rspd = rspd + 1
        f = open("C:/iruda/learn/"+message.content[4:]+".txt")
        lrn = f.read()
        f.close()

        lrn = lrn.split("`")
        await channel.send("```"+lrn[0]+"```\n`"+lrn[1]+"님이 등록하셨어요.`")

# 명령어 유효 확인
    if message.content.startswith("이루다 ") and rspd == 0 and server_status == 'operating':
        await channel.send("> 제가 대답할 수 있는게 없네요...\n> 혹시 '이루다 도움말'을 사용해서 다시 알아봐주실 수 있나요?")

app.run(token)
