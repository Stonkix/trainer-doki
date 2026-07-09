<?

require($_SERVER["DOCUMENT_ROOT"] . "/bitrix/header.php");
$APPLICATION->SetTitle("Тренажер для пользователей сервиса&nbsp;Доки");
$arItem = [
    'CODE' => 'doki',
    'DETAIL_PAGE_URL' => '/products/doki/',
    'COLOR' => 'skycyan',
    'NAME' => 'Доки',
    'PREVIEW_TEXT' => 'Сервис электронного документооборота с контрагентами',
    'TRAINER_URL' => '/trainer/astraldocs/',
]; ?>
    <style>
        main h1 {
            text-align: center;
            margin: 0 10vw;
        }

        .trainer-img {
            width: 100px;
            height: 100px;
        }

        .trainer-ul {
            list-style: none;
            text-align: center;
            margin: auto;
            padding: 0;
        }

        .btn-outline-<?=$arItem['COLOR']?> {
            color: #444444;
            border-color: transparent;
            width: 100%;
            padding: .7815rem 10vw !important;
        }
    </style>
    <div class="container my-48">
        <div class="d-flex">
            <img class="trainer-img m-auto"
                 src="<?= SITE_TEMPLATE_PATH ?>/assets/svg/products/<?= $arItem['CODE'] ?>.svg">
        </div>
    </div>
    <div class="container my-48">
        <div class="d-flex">
            <ul class="trainer-ul">
                <li class="pb-16">

                    <a class="shadow-sm btn btn-outline-<?= $arItem['COLOR'] ?>"
                       target="_blank" href="/trainer/astraldocs/invite.html">Как пригласить контрагентов начать с вами
                        ЭДО</a>

                </li>
                <li class="pb-16">

                    <a class="shadow-sm btn btn-outline-<?= $arItem['COLOR'] ?>"
                       target="_blank" href="/trainer/astraldocs/info_send.html">Как отправить электронный документ</a>

                </li>
                <li class="pb-16">

                    <a class="shadow-sm btn btn-outline-<?= $arItem['COLOR'] ?>"
                       target="_blank" href="/trainer/astraldocs/sgn.html">Как получить и подписать электронный
                        документ</a>

                </li>
                <li class="pb-16">
    
                        <a class="shadow-sm btn btn-outline-<?= $arItem['COLOR'] ?>"
                           target="_blank" href="/trainer/astraldocs/create.html">Как создать в 1С поступление</a>
    
                    </li>
                <li class="pb-16">
    
                        <a class="shadow-sm btn btn-outline-<?= $arItem['COLOR'] ?>"
                           target="_blank" href="/trainer/astraldocs/epd.html">ЭПД в Доки</a>
    
                    </li>
                </ul>

        </div>
    </div>
<?php
require($_SERVER["DOCUMENT_ROOT"] . "/bitrix/footer.php") ?>