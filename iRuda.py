import asyncio
import discord, os, re, random, sys, time, subprocess

app = discord.Client()

access_token = os.environ["BOT_TOKEN"]
token = access_token

@app.event
async def on_ready():
    print("이루다 봇이 다음과 같이 로그인합니다.")
    print(app.user.name)
    print(app.user.id)
    print("=====누출되지 않게 하십시오.=====")

    await app.change_presence(activity=discord.Game(name="'이루다 도움말'을 입력하세요!"))

    f = open("C:/iruda/log/system_log.txt", 'r', encoding="UTF8")
    log = f.read()
    f.close()

    now = time.localtime()
    now_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

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

# 기본명령어
    if message.content == "이루다":
        rspd = rspd + 1
        await channel.send("네, <@"+str(id)+">님! 저 여기있어요!\n당신이 있는 곳은 `#"+str(channel)+"` 이군요!")
        if auth == 'ad':
            await channel.send("```승인 ID : "+str(id)+"\n관리자로 정상식별 되었습니다.```")

    if message.content == "이루다 도움말":
        f = open("C:/iruda/help.txt", 'rt', encoding='UTF8')
        comm_help = f.read()
        f.close()

        await channel.send("도움말은 제가 DM으로 보내드릴테니, 확인해주세요!")

        user = app.get_user(int(id))

        embed = discord.Embed(title="이루다 베타 도움말", description=comm_help)
        await user.send(embed=embed)


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
        await channel.send("다음은 이루다 봇의 공식 사이트 주소예요.\n이루다 봇에 대한 자세한 정보를 보실수도 있고, 문제사항에 대해서 문의하실수도 있어요!\n\n공식사이트 바로가기 >> https://se701-2201.wixsite.com/irudabot")

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

    if message.content == "이루다 시계":
        rspd = rspd + 1
        await channel.send("현재 시각을 알려드릴게요. (이루다 봇 서버 시각입니다.)\n```KST "+now_time+"```")


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

# 돈 관련 명령어
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
                        
                        if int(my_money) >= int(message.content[31:]):
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
                            await channel.send("선물할 금액이 보유한 잔고를 초과해요.")
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

# 프로모션 코드 관련 명령어
    if message.content == "이루다 프로모션코드관리 승인대기":
        rspd = rspd + 1
        if auth == 'ad':
            f = open("C:/iruda/promtn/waiting.txt", 'r')
            wait = f.read()
            f.close()

            await channel.send("관리자님, 승인대기중인 프로모션코드는 `"+wait+"`개가 있어요.")
        else:
            await channel.send("해당 명령어는 관리자만 사용할 수 있어요.")

    if message.content == "이루다 프로모션코드관리 승인확인":
        rspd = rspd + 1
        if auth == 'ad':
            f = open("C:/iruda/promtn/waiting.txt", 'r')
            wait = f.read()
            f.close()

            f = open("C:/iruda/promtn/waiting.txt", 'w')
            f.write('0')
            f.close()

            f = open("C:/iruda/promtn/user.txt", 'r')
            uscode = f.read()
            f.close()

            uscode = int(uscode) + int(wait)
            uscode = str(uscode)

            f = open("C:/iruda/promtn/user.txt", 'w')
            f.write(uscode)
            f.close()

            await channel.send("관리자님, 승인대기중이였던 프로모션 코드 `"+wait+"`개가 승인처리 되었어요.\n현재 승인된 프로모션 코드는 총 `"+uscode+"`개예요.")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : 프로모션코드 승인처리")
            f.close()
        else:
            await channel.send("해당 명령어는 관리자만 사용할 수 있어요.")

    if message.content == "이루다 프로모션코드관리 승인거부":
        rspd = rspd + 1
        if auth == 'ad':
            f = open("C:/iruda/promtn/waiting.txt", 'r')
            wait = f.read()
            f.close()

            f = open("C:/iruda/promtn/waiting.txt", 'w')
            f.write('0')
            f.close()

            await channel.send("관리자님, 승인대기중이였던 프로모션 코드 `"+wait+"`개가 승인거부 되었어요.")

            f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
            f.write(log + "\n["+now_time+"] ID "+str(id)+" : 프로모션코드 승인거부")
            f.close()
        else:
            await channel.send("해당 명령어는 관리자만 사용할 수 있어요.")

    if message.content == "이루다 프로모션코드관리 코드사용":
        rspd = rspd + 1
        if auth == 'ad':
            f = open("C:/iruda/promtn/user.txt", 'r')
            uscode = f.read()
            f.close()

            if int(uscode) > 0:
                uscode = int(uscode) - 1
                uscode = str(uscode)

                f = open("C:/iruda/promtn/user.txt", 'w')
                f.write(uscode)
                f.close()

                await channel.send("관리자님, 등록되어있던 프로모션 코드 `1`개를 사용하여 이제 총 `"+uscode+"`개가 되었어요.")

                f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                f.write(log + "\n["+now_time+"] ID "+str(id)+" : 프로모션코드 코드사용")
                f.close()
            else:
                await channel.send("등록된 프로모션 코드가 `0`개예요. 프로모션 코드를 충전해주세요.")
        else:
            await channel.send("해당 명령어는 관리자만 사용할 수 있어요.")

    if message.content == "이루다 프로모션코드 구매":
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
            my_money = f.read()
            f.close()

            await channel.send("프로모션코드는 1개당 이루다 가상계좌 `10000000000000`원이예요.\n현재, <@"+str(id)+">님의 가상계좌 잔돈은 `"+my_money+"`원이에요.\n\n**프로모션 코드 구입을 확정하시려면, '이루다 프로모션코드 구매확정'명령어를 입력해주세요!")
        else:
            await channel.send("해당 명령어는 가상계좌가 있는 사용자만 사용할 수 있어요.")

    if message.content == "이루다 프로모션코드 구매확정":
        rspd = rspd + 1
        if os.path.isfile("C:/iruda/money/"+str(id)+".txt"):
            f = open("C:/iruda/money/"+str(id)+".txt", 'r')
            my_money = f.read()
            f.close()

            if int(my_money) >= 10000000000000:
                f = open("C:/iruda/promtn/waiting.txt", 'r')
                wait = f.read()
                f.close()

                f = open("C:/iruda/promtn/waiting.txt", 'w')
                wait = int(wait) + 1
                wait = str(wait)
                f.write(wait)
                f.close()

                f = open("C:/iruda/money/"+str(id)+".txt", 'w')
                f.write(str(int(my_money) - 10000000000000))
                f.close()

                await channel.send("`가상계좌에서 10000000000000원이 결제승인처리 되었습니다.`\n이루다 프로모션코드 `1`개가 결제되었어요. 결제승인된 프로모션코드는 추가적으로 개발자님의 승인을 받아야 하니, 승인이 완료될 때까지 조금만 기다려주세요.")

                user = app.get_user(500251192883150859)
                await user.send("주인님, 비활성화 프로모션 코드가 `"+wait+"`개 대기중이예요.")

                f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                f.write(log + "\n["+now_time+"] ID "+str(id)+" : 프로모션코드 구매")
                f.close()
            else:
                await channel.send("아직 가상계좌의 돈이 부족해요. 프로모션코드를 사기까지 `"+str(10000000000000 - int(my_money))+"`원 남았어요.")
    
    if message.content.startswith("이루다 프로모션코드 ") and rspd == 0:
        rspd = rspd + 1        
        if not(" " in message.content[11:]):
            f = open("C:/iruda/promtn/promtncode.txt", 'rt', encoding="UTF8")
            code = f.read()
            f.close()

            rccode = message.content[11:]
            length = len(message.content[11:])

            if rccode + "." in code:
                getfind = code.find(rccode)
                code = code[:getfind] + code[getfind+length+1:]                
                f = open("C:/iruda/promtn/promtncode.txt", 'w')
                f.write(code)
                f.close()

                f = open("C:/iruda/promtn/waiting.txt", 'r')
                wait = f.read()
                f.close()

                f = open("C:/iruda/promtn/waiting.txt", 'w')
                wait = int(wait) + 1
                wait = str(wait)
                f.write(wait)
                f.close()

                await channel.send("해당 프로모션 코드 [`"+rccode+"`](이)가 일치하여 프로모션 코드 승인대기목록에 추가되었어요.\n현재 승인대기 코드가 1개 추가되어 총 `"+wait+"`개가 되었어요.")
                
                f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                f.write(log + "\n["+now_time+"] ID "+str(id)+" : ["+rccode+"](을)를 프로모션코드로 등록")
                f.close()

                user = app.get_user(500251192883150859)
                await user.send("주인님, 비활성화 프로모션 코드가 `"+wait+"`개 대기중이예요.")
            else:
                await channel.send("존재하는 않는 프로모션 코드이거나, 이미 사용된 프로모션 코드일 수 있어요. 다시한번 확인해 주세요.")

                f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
                f.write(log + "\n["+now_time+"] ID "+str(id)+" : ["+rccode+"]의 프로모션코드 등록실패")
                f.close()
        else:
            await channel.send("해당 프로모션 코드에 띄어쓰기가 포함되어 있어요. 프로모션 코드를 다시한번 확인해주세요.")

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

# 명령어 유효 확인
    if message.content.startswith("이루다 ") and rspd == 0 and server_status == 'operating':
        await channel.send("> 제가 대답할 수 있는게 없네요...\n> 혹시 '이루다 도움말'을 사용해서 다시 알아봐주실 수 있나요?")

app.run(token)
